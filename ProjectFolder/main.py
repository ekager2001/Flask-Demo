import time
from tracemalloc import start
from flask import Blueprint, render_template, redirect, request, send_file, session
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import zipfile
import os
from ProjectFolder.models import History
from . import db
from flask import current_app
from .Components.PDFconverter import PDFconverter
import os
import uuid

main = Blueprint('main', __name__)

#Not my code taken and adpted from Flask website: https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

##Original Code
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect("/profile")
    else:
        return redirect("/login")

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/fileUpload')
@login_required
def textInput():
    return render_template('fileUpload.html')

@main.route('/textInputWebscrape')
@login_required
def textUpload():
    return render_template('textInputWebscrape.html')

@main.route('/fileUploadWebScrape')
@login_required
def fileUpload():
    return render_template('fileUploadWebScrape.html')

@main.route('/recruit')
@login_required
def recruiter():
    return render_template('recruiter.html')

@main.route('/feedback', methods=['GET','POST'])
def feedback():
    start = time.time()
    error= None
    if request.method == 'GET':
        return redirect('/')

    if request.method == 'POST':
        #Variables!
        type = request.form['Form']
        if type != "multiFile" and type !="JobDescInput":
            position= request.form['position']
            location= request.form['location']
            searchQ =(position, location)
        if type == "JobDescInput":
            title = request.form['title']
            company = request.form['company']
            jobDesc = request.form['text']
        resumeSkills = []      
        html=""
        rawtext=""
        jobs=None
        skill_pattern_path = "ProjectFolder/Components/ModelData/jz_skill_patterns.jsonl"

        if type=="textInput":
            rawtext = request.form.get('text')
        #Not my code gained from Flask website: https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
        if type=="file" or type == "JobDescInput":
            file = request.files['CVpdf']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            else: #Copied code ends here ^
                return redirect("/File")
            PDFconvert = PDFconverter()
            rawtext = PDFconvert.extract(file)
        if type=="multiFile":
            rawtext = request.form.get('text')
            FileList = request.files.getlist("pdfList")
            listCandidates = []
            #Not my code gained from Flask website: https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
            for file in FileList:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))    
                else: #Copied code ends here ^
                    return redirect("/recruit") 
                PDFconvert = PDFconverter()
                filename = file.filename
                print(filename)
                text = PDFconvert.extract(file) 
                listCandidates.append((filename[:-4].replace("_", " "),text))
    # return render_template('feedback.html', rawtext=rawtext, resumeSkills=resumeSkills, html=html)
       
        #Refactor'd code to use an abstract Analyser Class! 
        outputs = None

        AN = current_app.config['Analyser']
        tuple = AN.skillsExtract(rawtext) #rawtext is the CV for job applier, and JobDesc for recruiter
        html = tuple[0]    
        entitySkills = tuple[1] 
        unique = str(uuid.uuid4())
        if type=="multiFile":
            inputName = "Job Description"
            try:
                outputs = AN.rankCandidates(listCandidates, entitySkills)
            except:
                return redirect("/") 
            string = "Candiates here:"
            f = open(os.path.join(current_app.config['DOWNLOAD_FOLDER'], unique+".txt"), "w", encoding="utf-8")
            f.write("Job description: \n")
            f.write(rawtext+"\n")
            f.write(string)
            for output in outputs:
                f.write(output.name + "\n")
                f.write("match percentage: "+str(output.match)+"% \n")
                f.write("Skills:\n")
        
                #Applicant Technical Skills
                for skill  in output.skillsMet:
                     if skill.type == "SKILL": f.write(skill.skill+"\n")
                f.write("Skills present:\n")
                for skill  in output.skillsNotMet:
                     if skill.type == "SKILL": f.write(skill.skill+"\n")

                #Applicant Soft Skills
                f.write("Soft Skills missing:\n")
                for skill  in output.skillsMet:
                     if skill.type == "SOFT-SKILL": f.write(skill.skill+"\n")
                f.write("Skills present:\n")
                for skill  in output.skillsNotMet:
                    if skill.type == "SOFT-SKILL": f.write(skill.skill+"\n") 
            f.close()
            item = History(userID = current_user.id, fileName = unique+".txt")
            db.session.add(item)
            db.session.commit()
        elif type == 'textInput' or type == "file":
            inputName = "CV"
            try:
                outputs = AN.webScrape(searchQ, entitySkills)
            except:
                return redirect("/") 
        #Suffered problem with too long stuff like this:
            string = "You searched for Job: {} \nLocation: {}"
            string = string.format(searchQ[0],searchQ[1])
            f = open(os.path.join(current_app.config['DOWNLOAD_FOLDER'], unique+".txt"), "w", encoding="utf-8")
            f.write(string)
            for output in outputs:
                f.write("\n"+ output.title  +" \n")
                f.write(output.company + "\n")
                f.write("match percentage: "+str(output.match)+"% \n")
                f.write("Skills missing:\n")
                for skill  in output.skillsNotMet:
                     if skill.type == "SKILL": f.write(skill.skill+"\n")
                f.write("Soft Skills missing:\n")
                for skill  in output.skillsNotMet:
                    if skill.type == "SOFT-SKILL": f.write(skill.skill+"\n") 
            f.close()
            item = History(userID = current_user.id, fileName = unique+".txt")
            db.session.add(item)
            db.session.commit()
        else: 
            jobInfo = [title,company,jobDesc]
            inputName = "CV"
            outputs = AN.compare(jobInfo, entitySkills)
            f = open(os.path.join(current_app.config['DOWNLOAD_FOLDER'], unique+".txt"), "w", encoding="utf-8")
            for output in outputs:
                f.write("\n"+ output.title  +" \n")
                f.write(output.company + "\n")
                f.write("match percentage: "+str(output.match)+"% \n")
                f.write("Skills missing:\n")
                for skill  in output.skillsNotMet:
                     if skill.type == "SKILL": f.write(skill.skill+"\n")
                f.write("Soft Skills missing:\n")
                for skill  in output.skillsNotMet:
                    if skill.type == "SOFT-SKILL": f.write(skill.skill+"\n") 
            f.close()
            item = History(userID = current_user.id, fileName = unique+".txt")
            db.session.add(item)
            db.session.commit()
    end = time.time()
    delta = (end - start)
    #print("{:.2f} seconds"delta)
    return render_template('feedback.html',inputName=inputName, entitySkills=entitySkills, html=html, outputs=outputs)

@main.route('/download', methods=['GET','POST'])
#Credit goes to Bala Mrugan NG for download function:
# https://medium.com/analytics-vidhya/receive-or-return-files-flask-api-8389d42b0684
def download():
    userFiles = []
    userHistory = History.query.filter_by(userID=current_user.id).all()
    for item in userHistory:
        userFiles.append(item.fileName)
    # Zip file Initialization
    zipfolder = zipfile.ZipFile(current_app.config['DOWNLOAD_FOLDER']+"/"+'History.zip','w', compression = zipfile.ZIP_STORED) # Compression type 

    # zip all the files which are inside in the folder
    for root, dirs, files in os.walk(current_app.config['DOWNLOAD_FOLDER']+"/"):
        for file in files:
            if file in userFiles:
                zipfolder.write(current_app.config['DOWNLOAD_FOLDER']+"/"+file)
    zipfolder.close()
    downloadFolder = os.path.join(os.getcwd(),current_app.config['DOWNLOAD_FOLDER']) #get download folder
    downloadPath =  os.path.join(downloadFolder,'History.zip') #download folder
    return send_file(downloadPath,
            mimetype = 'zip', attachment_filename='History.zip',
            as_attachment = True)
