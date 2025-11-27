from app import create_app



# creating this as an entry point used to start the flask app.
app = create_app()



if __name__ == '__main__':
    app.run(debug=True)