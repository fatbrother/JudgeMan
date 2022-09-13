from app import app
import app.pages as pages

if __name__ == '__main__':
    pages.registerBlueprints(app)
    app.run(debug=True)