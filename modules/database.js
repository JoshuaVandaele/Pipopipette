const fs = require('fs');

const dataFolder = "./databases/";

/* Module used to store data in a file */

module.exports = {
  readFile: async function(filePath){
    try{
      const data = await fs.promises.readFile(dataFolder + filePath, 'utf-8');
      return JSON.parse(data);
    }catch(err){
      throw `Error while reading saved file : ${err}`;
    }
  },

  writeFile: async function(filePath, data){
    try{
      await fs.promises.writeFile(dataFolder + filePath, JSON.stringify(data));
    }catch(err){
      throw `Error while writing in a saved file : ${err}`;
    }
  },

  appendToFile: async function(filePath, data){
    try{
      await fs.promises.appendFile(dataFolder + filePath, JSON.stringify(data));
    }catch(err){
      throw `Error while appending to a saved file : ${err}`;
    }
  },

  clearFile: async function(filePath){
    try{
      await fs.promises.writeFile(dataFolder + filePath, '');
    }catch(err){
      throw `Error while deleting from a saved file : ${err}`;
    }
  },

  createFileWithDefaults: async function(filePath, defaults){
    try{
      await fs.promises.writeFile(dataFolder + filePath, JSON.stringify(defaults));
    }catch(err){
      throw `Error while creating file with defaults : ${err}`;
    }
  }
};
