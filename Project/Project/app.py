from app import app, db
from app.models import User, Comparison


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User':User, 'Comparison':Comparison}


if __name__ == '__main__':
    app.run(debug=True)