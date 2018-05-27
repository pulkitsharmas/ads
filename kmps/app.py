from flask import Flask, url_for, request, redirect, render_template, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_uploads import UploadSet, IMAGES, configure_uploads
from dbsetup import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kmpsdb.db'
app.config['SECRET_KEY'] = 'cow-mata-ki-jai'
app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads/'
app.config['UPLOADED_IMAGES_URL'] = 'static/uploads/'

db.init_app(app)
lm = LoginManager(app)
images = UploadSet('images',IMAGES)
configure_uploads(app, images)

from models import User, Organization, Department, Brequest, Docq, Rejects
from forms import ARForm, ChangePass, EditProfile, LoginForm, RegisterAdmin, DepartmentNewEdit, DeleteForm, UserAdd, RequestAdd, OptUploadForm, UploadForm

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/login')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.password==form.password.data:
			return render_template('login.html', form=form, toasty="Invalid Login Details!")
		login_user(user)
		if user.type==1:
			return redirect(url_for('admin_home'))
		elif user.type==3:
			return redirect(url_for('user_home',id=user.id))
		elif user.type ==2 and not user.department.isfin:
			return redirect(url_for('manager_home',id=user.id))
		else:
			return redirect(url_for('fmanager_home',id=user.id))
	print form.email.errors
	print form.password.errors
	return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
	form = RegisterAdmin()
	print form.validate_on_submit()
	if form.validate_on_submit():
		print "here"
		org = Organization(name = form.oname.data)
		dept = Department.query.filter_by(name = 'Admin').first()
		if dept is None:
			dept = Department(name='Admin',description='Administrator of Organization.', isfin=False, organization=org)
			db.session.add(dept)
			db.session.commit()
		db.session.add(org)
		db.session.commit()
		user = User(name=form.name.data, email=form.email.data, password=form.password.data, 
			type=1, profile_filename='default256.png', profile_url='static/default256.png', 
			department=dept, organization=org)
		db.session.add(user)
		db.session.commit()
		flash('Registration Completed.')
		return redirect('/login')

	return render_template('register.html',form=form)

@app.route('/admin/home')
@login_required
def admin_home():
	return render_template('/admin/home.html')

@app.route('/admin/departments')
@login_required
def department_list_all():
	depts = Department.query.filter_by(organization=current_user.organization).all()
	return render_template('/admin/dept_list_all.html',depts=depts)

@app.route('/admin/departments/add', methods=['GET','POST'])
def department_add():
	form = DepartmentNewEdit()
	if form.validate_on_submit():
		dept = Department(name=form.name.data, description=form.description.data, isfin=form.isfin.data, 
			organization=current_user.organization)
		db.session.add(dept)
		db.session.commit()
		flash('Department Added.')
		return redirect(url_for('department_list_all'))
	return render_template('/admin/dept_new.html', form=form)

@app.route('/admin/departments/<int:did>/edit', methods=['GET','POST'])
@login_required
def department_edit(did):
	form = DepartmentNewEdit()
	if form.validate_on_submit():
		dept = Department.query.filter_by(did=did).first()
		dept.name = form.name.data
		dept.description = form.description.data
		dept.isfin = form.isfin.data
		dept.organization = current_user.organization
		db.session.add(dept)
		db.session.commit()
		flash('Department Edited Successfully.')
		return redirect(url_for('department_list_all'))
	return render_template('/admin/dept_edit.html', form=form)

@app.route('/admin/departments/<int:did>/delete', methods=['GET','POST'])
@login_required
def department_delete(did):
	form = DeleteForm()
	if form.validate_on_submit():
		dept =  Department.query.filter_by(did=did).first()
		db.session.delete(dept)
		db.session.commit()
		flash('Department Deleted.')
		return redirect(url_for('department_list_all'))
	return render_template('/admin/dept_delete.html', form=form)

@app.route('/admin/employees', methods=['GET','POST'])
@login_required
def employee_list_all():
	dept = Department.query.filter_by(organization=current_user.organization).all()
	if dept is None or len(dept)==0 or (len(dept)==1 and dept[0].name=='Admin'):
		return render_template('/admin/emp_list_all.html',dept=False)
	else:
		emps = User.query.filter_by(organization=current_user.organization).all()
		return render_template('/admin/emp_list_all.html',emps=emps,dept=dept)


@app.route('/admin/employees/add', methods=['GET', 'POST'])
@login_required
def employee_add():
	form = UserAdd()
	form.dept_id.choices = [ (d.did, d.name) for d in Department.query.filter_by(organization=current_user.organization) ]
	print form.type.errors
	if form.validate_on_submit():
		dept = Department.query.filter_by(did=form.dept_id.data).one()
		user=User(name=form.name.data,email=form.email.data,password="1234567",type=form.type.data,
			profile_filename='default256.png', profile_url='static/default256.png',department=dept,
			organization=current_user.organization)
		db.session.add(user)
		db.session.commit()
		flash('User Added.')
		return redirect(url_for('admin_home'))
	return render_template('/admin/emp_new.html',form=form)

@app.route('/admin/employees/<int:id>/edit', methods=['GET','POST'])
@login_required
def employee_edit(id):
	form = UserAdd()
	form.dept_id.choices = [(d.did, d.name) for d in Department.query.filter_by(organization=current_user.organization)]
	if form.validate_on_submit():
		emp=User.query.filter_by(id=id).one()
		emp.name = form.name.data
		emp.email = form.email.data
		dept = Department.query.filter_by(did=form.dept_id.data).one()
		emp.department=dept
		emp.type = form.type.data
		db.session.add(emp)
		db.session.commit()
		flash('User edited successfully.')
		return redirect(url_for('employee_list_all'))
	return render_template('/admin/emp_edit.html', form=form)

@app.route('/admin/employees/<int:id>/delete', methods=['GET','POST'])
@login_required
def employee_delete(id):
	form = DeleteForm()
	if form.validate_on_submit():
		user = User.query.filter_by(id=id).one()
		db.session.delete(user)
		db.session.commit()
		flash('User Deleted.')
		return redirect(url_for('employee_list_all'))
	return render_template('/admin/emp_delete.html',form=form)

@app.route('/u/<int:id>/r', methods=['GET','POST'])
@login_required
def user_home(id):
	user = User.query.filter_by(id=id).first()
	reqs = Brequest.query.filter_by(user=user)
	return render_template('/emp/emp_req_list_all.html',reqs=reqs,user=user)

@app.route('/u/<int:id>/r/new', methods=['GET','POST'])
@login_required
def request_new(id):
	user = User.query.filter_by(id=id).first()
	managers = User.query.filter_by(type=2,department=user.department).all()
	if len(managers) == 0:
		print "man none"
		flash("No managers in your department.")
		return redirect(url_for('user_home',id=id))
	fmans = db.session.query(User,Department).join(Department).filter(User.type==2, Department.isfin==True, User.organization==current_user.organization).all()
	if len(fmans) == 0:
		print "fman none"
		flash("No finance managers in your organization.")
		return redirect(url_for('user_home',id=id))
	print "none none"
	form = RequestAdd()
	form.man.choices = [(u.id, u.name) for u in managers]
	form.fman.choices = [(us[0].id, us[0].name) for us in fmans]
	if form.validate_on_submit():
		br = Brequest(title=form.title.data,description=form.description.data,ammount=form.ammount.data,
			status=1,user=current_user,man_id=form.man.data,fman_id=form.fman.data)
		db.session.add(br)
		db.session.commit()
		flash('Request Successfully Initiated.')
		return redirect(url_for('media_upload_new',id=user.id,rid=br.rid))
	return render_template('/emp/req_new_first.html',form=form)

@app.route('/u/<int:id>/r/<int:rid>/m/new', methods=['GET','POST'])
@login_required
def media_upload_new(id,rid):
	form = UploadForm()
	user = User.query.filter_by(id=id).one()
	br = Brequest.query.filter_by(rid=rid).one()
	imgs= Docq.query.filter_by(brequest=br)
	if form.validate_on_submit():
		filename = images.save(request.files['upload'])
		url = images.url(filename)
		doc = Docq(caption=filename,filename=filename,doc_url=url,brequest=br)
		db.session.add(doc)
		db.session.commit()
		flash('Uploaded Successfully.')
		return redirect(url_for('media_upload_new',id=user.id,rid=br.rid))
	return render_template('/emp/media_upload.html',form=form,imgs=imgs)


@app.route('/u/<int:id>/r/<int:rid>/delete', methods=['GET','POST'])
@login_required
def request_delete(id,rid):
	form = DeleteForm()
	if form.validate_on_submit():
		docq = Docq.query.filter_by(brequest_id=rid).all()
		for d in docq:
			db.session.delete(d);
			db.session.commit();
		br = Brequest.query.filter_by(rid=rid).one()
		db.session.delete(br)
		db.session.commit()
		flash('Request Deleted')
		return redirect(url_for('user_home',id=current_user.id))
	return render_template('/emp/req_delete.html',form=form)

@app.route('/u/<int:id>/r/<int:rid>/edit', methods=['GET','POST'])
@login_required
def request_edit(id,rid):
	form = RequestAdd()
	managers = User.query.filter_by(type=2,department=current_user.department).all()
	fmans = db.session.query(User,Department).join(Department).filter(User.type==2, Department.isfin==True, User.organization==current_user.organization).all()
	form.man.choices = [(u.id, u.name) for u in managers]
	form.fman.choices = [(us[0].id, us[0].name) for us in fmans]
	if form.validate_on_submit():
		req = Brequest.query.filter_by(rid=rid).one()
		req.title = form.title.data
		req.description = form.description.data
		req.ammount = form.ammount.data
		req.man_id = form.man.data
		req.fman_id = form.fman.data
		db.session.add(req)
		db.session.commit()
		flash('Request Edited Successfully')
		return redirect(url_for('media_upload_new',id=current_user.id,rid=rid))
	return render_template('/emp/req_edit.html',form=form)

@app.route('/u/<int:id>/r/<int:rid>/view', methods=['GET','POST'])
@login_required
def request_view(id,rid):
	req = Brequest.query.filter_by(rid=rid).one()
	imgs = Docq.query.filter_by(brequest=req).all()
	comments = Rejects.query.filter_by(brequest=req).all()
	return render_template('/emp/req_view.html',req=req,imgs=imgs,comments=comments)

@app.route('/m/<int:id>/r', methods=['GET', 'POST'])
@login_required
def manager_home(id):
	user = User.query.filter_by(id=id).first()
	reqs = Brequest.query.filter_by(status=1,man=user)
	return render_template('/manager/m_req_list_all.html',reqs=reqs,user=user)

@app.route('/fm/<int:id>/r', methods=['GET', 'POST'])
@login_required
def fmanager_home(id):
	user = User.query.filter_by(id=id).first()
	reqs = Brequest.query.filter_by(status=2,fman=user)
	return render_template('/manager/fm_req_list_all.html',reqs=reqs,user=user)


@app.route('/m/<int:id>/r/<int:rid>/view', methods=['GET','POST'])
@login_required
def man_request_view(id,rid):
	req = Brequest.query.filter_by(rid=rid).one()
	imgs = Docq.query.filter_by(brequest=req).all()
	comments = Rejects.query.filter_by(brequest=req).all()
	return render_template('/manager/m_req_view.html',req=req,imgs=imgs,comments=comments)

@app.route('/fm/<int:id>/r/<int:rid>/view', methods=['GET','POST'])
@login_required
def fman_request_view(id,rid):
	req = Brequest.query.filter_by(rid=rid).one()
	imgs = Docq.query.filter_by(brequest=req).all()
	comments = Rejects.query.filter_by(brequest=req).all()
	return render_template('/manager/fm_req_view.html',req=req,imgs=imgs,comments=comments)

@app.route('/m/<int:id>/r/<int:rid>/fwd', methods=['GET','POST'])
@login_required
def man_fwd(id,rid):
	req = Brequest.query.filter_by(rid=rid).one()
	form = ARForm()
	if form.validate_on_submit():
		cmt = Rejects(comment=form.comment.data,brequest=req)
		req.status = 2
		db.session.add(cmt)
		db.session.add(req)
		db.session.commit()
		flash('Request Forwarded.')
		return redirect(url_for('manager_home',id=id))
	return render_template('/manager/man_fwdrjt.html',form=form)

@app.route('/m/<int:id>/r/<int:rid>/rjt', methods=['GET','POST'])
@login_required
def man_rjt(id,rid):
	req = Brequest.query.filter_by(rid=rid).one()
	form = ARForm()
	if form.validate_on_submit():
		cmt = Rejects(comment=form.comment.data,brequest=req)
		req.status=0
		db.session.add(cmt)
		db.session.add(req)
		db.session.commit()
		flash('Request Rejected.')
		return redirect(url_for('manager_home',id=id))
	return render_template('/manager/man_fwdrjt.html',form=form)

@app.route('/fm/<int:id>/r/<int:rid>/fwd', methods=['GET','POST'])
@login_required
def fman_fwd(id,rid):
	req = Brequest.query.filter_by(rid=rid).one()
	form = ARForm()
	if form.validate_on_submit():
		cmt = Rejects(comment=form.comment.data,brequest=req)
		req.status = 3
		db.session.add(cmt)
		db.session.add(req)
		db.session.commit()
		flash('Request Approved.')
		return redirect(url_for('manager_home',id=id))
	return render_template('/manager/man_fwdrjt.html',form=form)

@app.route('/fm/<int:id>/r/<int:rid>/rjt', methods=['GET','POST'])
@login_required
def fman_rjt(id,rid):
	req = Brequest.query.filter_by(rid=rid).one()
	form = ARForm()
	if form.validate_on_submit():
		cmt = Rejects(comment=form.comment.data,brequest=req)
		req.status=0
		db.session.add(cmt)
		db.session.add(req)
		db.session.commit()
		flash('Request rejected.')
		return redirect(url_for('manager_home',id=id))
	return render_template('/manager/man_fwdrjt.html',form=form)


@app.route('/profile/<int:id>/view', methods=['GET','POST'])
@login_required
def myprofile(id):
	user= User.query.filter_by(id=id).one()
	return render_template('profile.html',user=user)

@app.route('/profile/<int:id>/edit', methods=['GET','POST'])
@login_required
def editprofile(id):
	user= User.query.filter_by(id=id).one()
	form = EditProfile()
	if form.validate_on_submit():
		user.name= form.name.data
		user.email = form.email.data
		db.session.add(user)
		db.session.commit()
		flash('Profile Successfully edited.')
		return redirect(url_for('myprofile',id=id))
	return render_template('editprofile.html',user=user, form=form)

@app.route('/profile/<int:id>/edit/pass', methods=['GET','POST'])
@login_required
def changepass(id):
	user= User.query.filter_by(id=id).one()
	form = ChangePass()
	if form.validate_on_submit():
		if form.old.data != user.password:
			return redirect(url_for('changepass',id=id))
		user.password = form.new.data
		db.session.add(user)
		db.session.commit()
		flash('Password Changed.')
		return redirect(url_for('myprofile',id=id))
	return render_template('changepass.html',user=user, form=form)

@app.route('/profile/<int:id>/edit/pic', methods=['GET','POST'])
@login_required
def changepic(id):
	user= User.query.filter_by(id=id).one()
	form = UploadForm()
	print form.validate_on_submit()
	if form.validate_on_submit():
		filename = images.save(request.files['upload'])
		url = images.url(filename)
		user.profile_url = url
		user.profile_filename= filename
		db.session.add(user)
		db.session.commit()
		flash('Profile Picture Changed.')
		return redirect(url_for('myprofile',id=id))
	return render_template('changepic.html',user=user, form=form)


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)