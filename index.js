"use-strict";

//Modules import
const CONFIG = require('./config.js');

const express = require('express');
const bodyParser = require('body-parser');

const printLogo = require("./modules/printLogo.js");
const gameAPIRoutes = require('./modules/gameApi.js');
const databaseManager = require('./modules/database.js');

//Express initialization
const app = express();
app.use(bodyParser.json());//Body parser used
app.use(bodyParser.urlencoded({ extended: true }));

gameAPIRoutes(app);//We can define some API routes here
const port = 3000;

//Default routes
app.get('/', (req, res) => {
  res.send('Hello World!');
});


//Starting the server
app.listen(port, '0.0.0.0', () => {
  console.log(`Le serveur est démarré sur le port ${port}`);
  databaseManager.createFileWithDefaults(CONFIG.DATABASE_NAME);
  printLogo();
});
