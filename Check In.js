const CheckIn = SpreadsheetApp.getActive().getSheetByName("Intake Form");
assetCol = findHeader('Lakers ####');
retUserCol = findHeader('Returner\'s Email');
problemCol = findHeader('Faulty Items');
devicesInCol = findHeader('Return Type');
categoryCol = findHeader('Return Category');
chargeCol = findHeader('Price');
explCol = findHeader('Explanation');

function latestEntry(column) {
  value = CheckIn.getRange(2, column, 1, 1).getValue().toString();
  return value
};


function checkIn() {
  // Logger.log('Starting Check In Process!')
  latestFirst(CheckIn);
  Logger.log(devicesInCol);
  CheckIn.activate()
  let devicesIn = latestEntry(devicesInCol);
  Logger.log(devicesIn);
  let faulty = latestEntry(problemCol);
  let explanation = latestEntry(explCol);
  let userMail = latestEntry(retUserCol);
  let userName = GAM.getUserName(userMail);
  var deviceTag;

  // Logger.log(devicesInCol);
  if (devicesIn.includes('Charger')) {
    ACC.charger(userName, 'in');
      Logger.log(latestEntry(findHeader('Charger Works')))
    if (latestEntry(findHeader('Charger Works')) === 'false') {
      faulty = faulty + getFormPrice('Charger');
    }
  } 
  Logger.log(faulty);
  
  let intookDevTag = latestEntry(assetCol).slice(-3); // !!! CURRENTLY SLICES LAST THREE FOR PRE-1000 IDS !!!

  if (intookDevTag !== '') {
    Logger.log(intookDevTag);
    let checkForDevice = searchAssetDB(intookDevTag)
    let deviceId = checkForDevice;

    if (!faulty || faulty === getFormPrice('Charger')) {
      if (checkForDevice === `${intookDevTag} could not be found in the Database Sheet`) {
        // Logger.log(`${intookDevTag} could not be found in Asset DB`)
        LOG.addTxn(`Attempted return of device ${intookDevTag} and device was not found`, 'failure')
        return
      }

      // Logger.log('No device faults found!')

      LGN.reserves(deviceId, explanation);
    } else {
    // Logger.log('Device was missing or damaged!');
    LGN.sickBay(deviceId, faulty, explanation)
    }

    ACC.removeDevice(`Lakers ${intookDevTag}`);

    deviceTag = `Lakers ${intookDevTag}`
    let deviceObj = GAM.getDevice(deviceId);
    if (deviceObj.annotatedUser !== userMail) {
      diffUsers(userMail, deviceTag, deviceObj.annotatedUser)
    }
  
  } else {
    thxCharger(userMail)
  }
    if (devicesIn == 'Chromebook AND Charger') {
      deviceTag = deviceTag + "/charger"
    }
    ACC.faultCharge(userMail, faulty, deviceTag);
  
}

function hehehuhu() {
  let priceOfOneDollar = getFormPrice('Charger')
  Logger.log(priceOfOneDollar);
}


function findHeader (q) {
  var Current = SpreadsheetApp.getActive().getActiveSheet();
  var headers = Current.getRange(1, 1, 1, Current.getLastColumn()).getValues()[0];
  // Logger.log(headers)
  return headers.findIndex((element) => element.startsWith(q))+1
};

function latestFirst(sheet) {
  SpreadsheetApp.setActiveSheet(sheet);
  let timeIndex = findHeader('Timestamp');
  sheet.sort(timeIndex, false);
};



//@OnlyCurrentDoc

function onOpen() {
 SpreadsheetApp.getUi()
  .createMenu("Tech Dept. Options")
  .addItem("Check In Asset", "showCheckInForm")
  .addItem("Update Prices", "populateQuestions")
  .addToUi();
}

function showCheckInForm() {
 SpreadsheetApp.getUi().showSidebar(HtmlService.createHtmlOutputFromFile("checkInForm.html").setTitle("Enter Assignment Information"));
}

function populateQuestions() {
  var form = FormApp.openByUrl('https://docs.google.com/forms/d/1KifzDMi_XmAhaS8St8O38eaOZvOPrQFoo43Wq05k14Y/edit');
  var googleSheetsQuestions = getQuestionValues()
  var itemsArray = form.getItems();
  itemsArray.forEach(function(item){
    googleSheetsQuestions[0].forEach(function(header_value,header_index) {
      if (header_value == item.getTitle ())
      {
        var choiceArray = [];
        for (j = 1 ; j < googleSheetsQuestions.length; j++)
          {
            (googleSheetsQuestions[j][header_index] != '') ? choiceArray.push(googleSheetsQuestions[j][header_index]) : null;
          }
        item.asCheckboxItem().setChoiceValues(choiceArray);
      }
    });
  });
}


function getQuestionValues() {
  var questionSheet = SpreadsheetApp.getActive().getSheetByName('Prices')
  var returnData = questionSheet.getDataRange().getValues();
  // Logger.log(returnData);

  return returnData;
};