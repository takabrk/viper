const electron = require('electron');
//const cp = require('child_process');
const {spawn} = require('child_process');
const url = require('url');
const path = require('path');
const viper = electron.app;
const browser_window = electron.BrowserWindow;
let mainWindow;
let URL;

var open_window = function(URL){
    main_window = new browser_window({
        width:1000,
        height:720
    });
    main_window.loadURL(URL);
    //let subpy = cp.spawn('python',['./index.py']);
    spawn('/bin/sh',['-c','./start_server']);
    main_window.on('closed',function(){
        main_window = null;
        //subpy.kill('SIGINT');
    });
};
viper.on('ready',function(){
   open_window(url.format({
       pathname:path.join(__dirname,'index.html'),
       protocol : 'file:',
       slashes:true
   }));
   //open_window('http://localhost:5000');
});
viper.on('window-all-closed',function(){
    viper.quit();
});