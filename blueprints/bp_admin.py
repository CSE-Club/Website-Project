from datetime import datetime

from loader import db

from flask import Blueprint, render_template, redirect, session, flash

from models import Content
from forms.pages import EditPageForm, DelPageForm
from sqlalchemy import desc, asc

from util.auth import Auth

blueprint = Blueprint('bp_admin', __name__, url_prefix='/admin')

@blueprint.before_request
def check_auth():
    if not 'user' in session:
        return redirect('/login')

    if session['user'].priv_level >= Auth.member:
        return redirect('/members')

@blueprint.route('/')
def view_dashboard():
    return render_template('admin/admin.html')

@blueprint.route('/content')
def view_pages():
    pages = Content.query.order_by(asc(Content.url)).all()

    return render_template('admin/content/view_pages.html', pages=pages)

@blueprint.route('/content/add', methods=['GET', 'POST'])
def add_page():
    form = EditPageForm()

    if form.validate_on_submit():
        page = Content()

        page.title = form.title.data
        page.content_type = 'page'
        page.url = form.url.data.lower()
        page.data_blob = form.content.data
        page.created_by = session['user'].id
        page.created_on = datetime.now()
        page.edited_by = -1
        page.edited_on = datetime.utcfromtimestamp(0)
        page.required_priv_level = form.level.data
        page.show_in_nav = form.navigation.data

        db.session.add(page)
        db.session.commit()

        flash('Page "' + page.title + '" created.')

        return redirect('/admin/content')

    return render_template('admin/content/edit_page.html', action='Creating New', title='Create Page', form=form)

@blueprint.route('/content/edit/<id>', methods=['GET', 'POST'])
def edit_page(id):
    page = Content.query.get(id)

    if not page:
        return redirect('/admin/content')

    form = EditPageForm()

    if form.validate_on_submit():
        page.title = form.title.data
        page.url = form.url.data
        page.data_blob = form.content.data
        page.edited_by = session['user'].id
        page.edited_on = datetime.now()
        page.required_priv_level = form.level.data
        page.show_in_nav = form.navigation.data

        db.session.merge(page)
        db.session.commit()

        flash('Page "' + page.title + '" updated.')

        return redirect('/admin/content')

    else:
        form.title.data = form.title.data if form.title.data else page.title
        form.url.data = form.url.data if form.url.data else page.url
        form.content.data = form.content.data if form.content.data else page.data_blob
        form.level.data = form.level.data if form.level.data else str(page.required_priv_level)
        form.navigation.data = form.navigation.data if form.navigation.data else page.show_in_nav

        if form.errors.items():
            for field, errors in form.errors.items():
                for error in errors:
                    flash(getattr(form, field).label.text + ' - ' + error)

    return render_template('admin/content/edit_page.html', action='Editing', title='Edit Page', form=form)

@blueprint.route('/content/delete/<id>', methods=['GET', 'POST'])
def delete_page(id):
    page = Content.query.get(id)

    if not page:
        return redirect('/admin/content')

    form = DelPageForm()

    if form.validate_on_submit():
        db.session.delete(page)
        db.session.commit()

        flash("Page deleted.")

        return redirect('/admin/content')

    return render_template('admin/content/delete_page.html', title='Delete Page', page=page, form=form)