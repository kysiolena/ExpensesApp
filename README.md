# Expenses App (Flask API)

## DB Schema
[ExpensesApp Miro](https://miro.com/app/board/uXjVGKTBNoY=/?share_link_id=838534107549)

## Run 
```terminaloutput
    flask --app app --debug run
```

## Swagger API Documentations

[Flask-swagger](https://pypi.org/project/flask-swagger/)

Route: `/docs`

## Migrations

[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)

###  Create a migration repository  
```terminaloutput
    flask db init
```

###  Generate an initial migration  
```terminaloutput
    flask db migrate -m "Initial migration"
```

###  Apply the changes described by the migration script to your database  
```terminaloutput
    flask db upgrade
```

### See all the commands that are available
```terminaloutput
    flask db --help
```