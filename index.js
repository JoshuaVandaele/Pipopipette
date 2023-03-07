const express = require('express');

const printLogo = require("./modules/printLogo.js");

const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(port, () => {
  console.log(`Le serveur est démarré sur le port ${port}`);
  printLogo();
});
