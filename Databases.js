// jshint esversion: 9
// jshint laxbreak: true

let StudentDB = SpreadsheetApp.getActive().getSheetByName('Student DB');
let AssetDB = SpreadsheetApp.getActive().getSheetByName('Asset DB');
let AssetFields = SpreadsheetApp.getActive().getSheetByName('Valid Device Fields');



function usersToSheet() {
  let fields = StudentDB.getRange(1, 1, 1, StudentDB.getLastColumn()).getValues()[0];
  let userRange = GAM.getUserList(`isAdmin=false`, fields);
  for (let i = 0; i < userRange.length; i++) {
    for (let j = 0; j < userRange[i].length; j++) {
        if (typeof userRange[i][j] === "boolean") {
          var checkbox = SpreadsheetApp.newDataValidation()
            .requireCheckbox()
            .build();
          StudentDB.getRange(i+2, j+1).setDataValidation(checkbox);
        }
    }
  }
  StudentDB.getRange(2, 1, userRange.length, StudentDB.getLastColumn()).setValues(userRange);
}

function devicesToSheet() {
  let fields = AssetDB.getRange(1, 1, 1, AssetDB.getLastColumn()).getValues()[0];
  let deviceRange = GAM.getDevices(`status:"managed"`, fields);
  AssetDB.getRange(2, 1, deviceRange.length, AssetDB.getLastColumn()).clearDataValidations();
  for (let i = 0; i < deviceRange.length; i++) {
    for (let j = 0; j < deviceRange[i].length; j++) {
        if (typeof deviceRange[i][j] === "boolean") {
          var checkbox = SpreadsheetApp.newDataValidation()
            .requireCheckbox()
            .build();
          AssetDB.getRange(i+2, j+1).setDataValidation(checkbox);
          deviceRange[i][j] = false;
        }
        if (fields[j] === 'status') {
          AssetFields.getRange('D2').copyTo(AssetDB.getRange(i+2, j+1, 1, 1), SpreadsheetApp.CopyPasteType.PASTE_DATA_VALIDATION, false);
          AssetDB.getRange(i+2, j+1, 1, 1).setHorizontalAlignment("center");
        }
        if (fields[j] === 'Wipe?') {
          AssetFields.getRange('F2').copyTo(AssetDB.getRange(i+2, j+1, 1, 1), SpreadsheetApp.CopyPasteType.PASTE_DATA_VALIDATION, false)
        }
        if (fields[j].toString().includes('.date')) {
          AssetDB.getRange(i+2, j+1, 1, 1).setValue(new Date(deviceRange[i][j])).setNumberFormat("MM/dd/yyyy");
        }
    }
  }
  // Logger.log(AssetDB.getRange(1, 1, 1, AssetDB.getLastColumn()).getValues())
  // Logger.log(deviceRange[0])
  AssetDB.getRange(2, 1, deviceRange.length, AssetDB.getLastColumn()).setValues(deviceRange);
}

function usersFromSheet() {
  let fields = StudentDB.getRange(1, 1, 1, StudentDB.getLastColumn()).getValues()[0];
  let userRange = StudentDB.getRange(2, 1, StudentDB.getLastRow()-1, StudentDB.getLastColumn()).getValues();
  // Logger.log(fields);
  // Logger.log(userRange[0]);
  GAM.multiUpdateUser(fields, userRange);
}

function devicesFromSheet() {
  let fields = AssetDB.getRange(1, 1, 1, AssetDB.getLastColumn()).getValues()[0];
  let deviceRange = AssetDB.getRange(2, 1, AssetDB.getLastRow()-1, AssetDB.getLastColumn()).getValues().filter(row => row[2] == true);
  // Logger.log(fields);
  // Logger.log(deviceRange[0]);
  GAM.multiUpdateDevice(fields, deviceRange);
}

function searchAssetDB(q) {
  q = q.toString()
  // Logger.log('Checking AssetDB for ' + q);
  AssetDB.activate();
  let assetColIndex = findHeader('annotatedAssetId');
  let assetCol = AssetDB.getRange(2, assetColIndex, AssetDB.getLastRow()-1).getValues();

  var searchResult = assetCol.findIndex(element => element[0].toString().includes(q));
  // Logger.log('found in row ' + searchResult);

  if (searchResult === -1) {
    let deviceID = q + ' could not be found in the Database Sheet'
    // Logger.log('hello?');
    return deviceID
  } else {
    let deviceId = AssetDB.getRange(searchResult+2, 1).getValue();
    return deviceId
  }
};

function searchStudentDB(q) {
  q = q.toString()
  if (q.length < 5) {
    q = `Lakers ${q}`
  }
  // Logger.log('Checking StudentDB for ' + q);
  StudentDB.activate();
  let studentColIndex = findHeader('name.fullName');
  let studentCol = StudentDB.getRange(2, studentColIndex, StudentDB.getLastRow()-1).getValues();

  var searchResult = studentCol.findIndex(element => element[0].includes(q));

  if (searchResult === -1) {
    let studentMail = q + ' could not be found in the Database Sheet'
    // Logger.log(studentMail)
    return studentMail
  } else {
    // Logger.log('found in row ' + searchResult);
    let studentMail = StudentDB.getRange(searchResult+2, 1).getValue();
    // Logger.log(studentMail)
    return studentMail
  }
};

function wtf() {
  searchAssetDB('Lakers 606')
}


