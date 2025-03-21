import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash  
from app.models import UserProfile
from app.forms import LoginForm, UploadForm 
from flask import send_from_directory


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/upload', methods=['POST', 'GET'])
@login_required  
def upload():
    """Route to handle image uploads."""
    form = UploadForm()

    # Validate file upload on submit
    if form.validate_on_submit():
        photo = form.photo.data

        # Secure the filename and save the file
        filename = secure_filename(photo.filename)

        # Define the upload path (you should have app.config['UPLOAD_FOLDER'] defined)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(upload_path)

        flash('File Saved Successfully!', 'success')

        # Redirect the user to a route that displays all uploaded image files
        return redirect(url_for('home'))  # You can change this to 'files' later

    return render_template('upload.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    """Route to handle user login."""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = UserProfile.query.filter_by(username=username).first()

        if user is not None:
            if check_password_hash(user.password, password):
                login_user(user)

                flash('You have successfully logged in!', 'success')

                return redirect(url_for("upload"))
            else:
                flash('Invalid password. Please try again.', 'danger')
        else:
            flash('Username not found. Please try again.', 'danger')

    flash_errors(form)

    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    """Route to handle user logout."""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    """This callback loads the user by ID."""
    return UserProfile.query.get(int(user_id))


###
# Helper functions
###

# Flash errors from the form if validation fails
def flash_errors(form):
    """Flash form errors."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


def get_uploaded_images():
    """Helper function to retrieve list of uploaded image filenames."""
    
    # Ensure UPLOAD_FOLDER is configured in your app config:
    # app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    upload_folder = app.config['UPLOAD_FOLDER']

    uploaded_files = []

    # Walk through the uploads directory and collect file names
    for subdir, dirs, files in os.walk(upload_folder):
        for file in files:
            uploaded_files.append(file)

    return uploaded_files

@app.route('/uploads/<filename>')
@login_required
def get_image(filename):
    """Route to retrieve and return an uploaded image file."""
    
    # Define the absolute path to your uploads directory
    upload_folder = app.config['UPLOAD_FOLDER']
    
    # Return the file from the uploads directory
    return send_from_directory(upload_folder, filename)

@app.route('/files')
@login_required
def files():
    """Route to display all uploaded images."""
    
    # Get the list of uploaded image filenames
    uploaded_images = get_uploaded_images()

    # Render the files.html template, passing the list of images
    return render_template('files.html', images=uploaded_images)


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
