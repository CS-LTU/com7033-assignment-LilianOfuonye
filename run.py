from app import create_app



# App entry point with app initialization
app = create_app()



if __name__ == '__main__':
    app.run(debug=True)