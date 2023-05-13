const Accounts = SpreadsheetApp.getActive().getSheetByName("Student Accounts");
const Charges = SpreadsheetApp.getActive().getSheetByName("Charges");
const Secretaries = SpreadsheetApp.openByUrl('https://docs.google.com/spreadsheets/d/1r1TpiQxqGvsMmyTEi8vW4eSRs9tsG8X2rMdVvMo2XPo/edit#gid=0').getSheetByName('Tech Charges').activate();


const ACC = new (function () {
  this.addPoints = (user, retCat) => {;
    if (retCat === "Faulty/Returning") { points = 0; }
    if (retCat === "Unforeseeable Accident") { points = 1; }
    if (retCat === "Faulty/Returning") { points = 2; }

  }

  this.faultCharge = (userName, faultyOrMissing, device) => {
    if (!userName) {
      throw new Error('Please input user to charge!');
    }

    if (!device) {
      var device = 'charger'; 
    }

    if (typeof userName !== 'string') {
      userName = userName.toString();
    }

    if (userName.includes('@')) {
      userMail = userName;
      try {
        userName = GAM.getUserName(userMail);
      } catch (e) {
        // Logger.log(e);
        LOG.addTxn(`Failed attempt to charge non-existent user ${userMail}`, 'Google Failure')
        return
      }
    }

    if (!faultyOrMissing || faultyOrMissing == "") {
      // Logger.log(faultyOrMissing)
      // Logger.log(`${userName} has been assessed with 0 charges at this time.`)
      LOG.addTxn(`No charges were applied to ${userName} for their ${device}`, 'Acceptable Return')
      return
    }
    
    if (searchStudentDB(userName) === userName + ' could not be found in the Database Sheet') {
      LOG.addTxn(`Could not get ${userName} from the Student Database to charge them`, 'Database Failure')
      return
    }

    let itemsCharge = faultyOrMissing.match(/\d+/g).map(Number).reduce((partialSum, a) => partialSum + a, 0);

    let chargeFormula = `=if(indirect(address(row(), match(\"Resolved\", 1:1, 0), 1)), 0, ${itemsCharge})`;
    let itemFiller = /[\-\s]{3}|[\d]*/g;
    let items = faultyOrMissing.replaceAll(itemFiller, "");

    Charges.activate();
    Charges.insertRowsBefore(2, 1);
    Charges.getRange(2, findHeader('Student Full'), 1, 1).setValue(userName);
    Charges.getRange(2, findHeader('Broken or Missing'), 1, 1).setValue(items);
    Charges.getRange(2, findHeader('Resolved'), 1, 1).insertCheckboxes();
    Charges.getRange(2, findHeader('Remaining Charge'), 1, 1).setFormula(chargeFormula).setNumberFormat('_("$"* #,##0.00_);_("$"* \\(#,##0.00\\);_("$"* "-"??_);_(@_)');
    let chargeDateFormat = ["YYYY/MM/DD"];
    Charges.getRange(2, findHeader('Date')).setValue(new Date()).setNumberFormat(chargeDateFormat);

    Secretaries.getRange(1, 1, 1, 1).activate();
    Secretaries.insertRowsBefore(2, 1);
    Logger.log(SpreadsheetApp.getActiveSpreadsheet().getName())
    Secretaries.getRange(2, 3, 1, 1).setValue(userName.split(" ").shift())
    Secretaries.getRange(2, 2, 1, 1).setValue(userName.split(" ", 2)[1])
    Secretaries.getRange(2, 4, 1, 1).setValue(itemsCharge).setNumberFormat('"$"#,##0.00');
    let secretaryYear = (Number(currentSY())-1).toString() + '-' + (Number(currentSY())).toString();
    let secretaryDescription = `Tech - ${items} ${secretaryYear} SY`
    Secretaries.getRange(2, 7, 1, 1).setValue(secretaryDescription)
    let secretaryDateFormat = ["MM/DD/YYYY"];
    Secretaries.getRange(2, 1, 1, 1).setValue(new Date()).setNumberFormat(secretaryDateFormat)


    faultyChargeMessage(userMail, items, itemsCharge)
    LOG.addTxn(`Successfully charged ${userName} \$${itemsCharge} for their faulty or missing ${device} (` + textMultiples(items) + ")", 'User Charged')
  }

  this.charger = (user, inOrOut, dueDate) => {
    let currentAccount = Accounts.createTextFinder(user).matchEntireCell(true).findAll()
    for (let i = 0; i < currentAccount.length; i++) {
      let row = currentAccount[i].getRow();
      let currChgsOut = Accounts.getRange(row, 5, 1, 1)
      let datesList = Accounts.getRange(row, 6, 1, 1);
      let currentDates = datesList.getValue().toString().trim().split(",").sort().reverse();
      // Logger.log(currentDates);
      if (inOrOut != 'in') {
        newNum = currChgsOut.getValue() + 1;
        newDates = currentDates.splice(currentDates.length, 0, dueDate).sort().reverse().join(",");
      } else {
        newNum = currChgsOut.getValue() - 1;
        // Logger.log(currentDates.toString());
        newDates = currentDates.splice(currentDates.indexOf(Math.min(...currentDates.map(currentDate => new Date(currentDate)))), 1);
        // Logger.log(newDates.toString());
        // Logger.log(newDates.length);
        datesList.setValue(currentDates.join(",").toString().trim());
      }
      currChgsOut.setValue(Math.max(newNum, 0));
    }

  }

  this.addAccount = (user, deviceTag, dueDate, ifCharger) => {
    // let stuEmail = user
    // let stuName = GAM.getUserName(user)
    // let firstDevOut = deviceTag
    // Accounts.addRows(2, 1)
    // if(ifCharger == 'true') {
    // ACC.chargerNum = (user, out, 1)
    // } else { Accounts.getRange(2, 5, 1, 1).setValue('0')
  }

  this.addDevice = (user, deviceTag, dueDate) => {
    // if (!Accounts.includes(user))
    // ACC.addAccount(user, deviceTag)
    // Accounts.getRange
  }

  this.removeDevice = (deviceTag) => {
    let currentAccount = Accounts.createTextFinder(deviceTag).matchEntireCell(true).findAll()
    for (let i = 0; i < currentAccount.length; i++) {
      let foundUsr = currentAccount[i].getRow()
      let foundDev = currentAccount[i].getColumn()

      let nowDev = Accounts.getRange(foundUsr, foundDev, 1, 2)
      let nextDev = Accounts.getRange(foundUsr, foundDev+2, 1, 2)
      if (!nextDev) {
        nowDev.setValues([["", ""]]);
      } else {
        nextDev.moveTo(nowDev);
      }
    }
  }

  this.report = (userMail) => {
    let userRow = Accounts.createTextFinder(userMail).matchEntireCell(true).findNext().getRow();
    var accountDevices = [];
    var report;
    let devsReport;

    for (let i = 0; i < 3; i++) {
      let deviceNum = (2 * i) + 7;
      // Logger.log(deviceNum);
      let deviceName = Accounts.getRange(userRow, deviceNum, 1, 1).getValue().toString();
      // Logger.log(deviceName);

      let deviceDue = new Date(Accounts.getRange(userRow, deviceNum+1, 1, 1).getValue()).toDateString();
      if (deviceDue == 'Invalid Date') {
        deviceDue = 'end of year'
      }
      if (deviceName) {
        accountDevices.push(deviceName + " (due " + deviceDue + ")")
      } else break;
      
    }

    Logger.log(accountDevices)
    if (accountDevices.length === 0) {
      Logger.log('length was 0')
      devsReport = 'No devices'
    } else if (accountDevices.length === 1) {
      Logger.log('length was 1')
      devsReport = accountDevices
      Logger.log(devsReport)
    } else {
      Logger.log('length was more')
      devsReport = accountDevices.join("\r\n\t");
    }
      Logger.log(devsReport);

    
    // Logger.log('made it past devices!')
    let chgsDates = Accounts.getRange(userRow, 6, 1, 1).getValue();
      // Logger.log(chgsDates);

    if (!chgsDates) {
      numChgsOut = 0; 
    } else if (typeof chgsDates !== 'string') {
      chgsDates = new Date(chgsDates).toDateString();
      numChgsOut = chgsDates.toString().split(',').length;
    } else {
      numChgsOut = chgsDates.toString().split(',').length;
    }

    // Logger.log(numChgsOut)
    if (numChgsOut !== 0) {
      chgsReport = `and ${numChgsOut} charger(s) out (due ` + textMultiples(chgsDates) +").";
      // Logger.log(chgsReport);
    } else {
      chgsReport = `and no chargers currently checked out.`
    }


    if (devsReport == 'No devices') {
      report = "\t" + devsReport + " " + chgsReport;
    } else {
      report = "\t" + devsReport + "\r\n\t" + chgsReport;
    }
    
    // Logger.log(report)
   
    return report
  }

  this.overDue = (currentAccount) => {
    if (!currentAccount) {
      throw new Error('Please input information to process!');
    }
    let currentUser = currentAccount.shift();
    Logger.log(currentAccount)
    let itemsCharge = Number(0);
    currentAccount.forEach((item) => {
      if (item.toString().includes('charger')) {
        item = item + " - " + Number(getFormPrice('Charger').match(/\d+/g))
        itemsCharge += Number(getFormPrice('Charger').match(/\d+/g))
      } else {
        item = item + " - " + Number(getFormPrice('Chromebook').match(/\d+/g))
        itemsCharge += Number(getFormPrice('Chromebook').match(/\d+/g))
        }
      Logger.log(item)
    })
    // Logger.log(currentUser);
    // Logger.log(currentAccount.toString());
    // Logger.log('hi');
    // itemsCharge = currentAccount.toString().match(/\d+/g).map(Number).reduce((partialSum, a) => partialSum + a, 0);
    Logger.log(itemsCharge);

    let chargeFormula = `=if(indirect(address(row(), match(\"Resolved\", 1:1, 0), 1)), 0, ${itemsCharge})`;
    // let itemFiller = /[\-\s]{3}|[\d]*/g;
    let items = currentAccount.toString()

    Charges.activate();
    Charges.insertRowsBefore(2, 1);
    let currentUserName = GAM.getUserName(currentUser)
    Charges.getRange(2, findHeader('Student Full'), 1, 1).setValue(currentUserName);
    Charges.getRange(2, findHeader('Broken or Missing'), 1, 1).setValue(items);
    Charges.getRange(2, findHeader('Resolved'), 1, 1).insertCheckboxes();
    Charges.getRange(2, findHeader('Remaining Charge'), 1, 1).setFormula(chargeFormula).setNumberFormat('_("$"* #,##0.00_);_("$"* \\(#,##0.00\\);_("$"* "-"??_);_(@_)');
    let chargeDateFormat = ["YYYY/MM/DD"];
    Charges.getRange(2, findHeader('Date')).setValue(new Date()).setNumberFormat(chargeDateFormat);

    Secretaries.getRange(1, 1, 1, 1).activate();
    Secretaries.insertRowsBefore(2, 1);
    Logger.log(SpreadsheetApp.getActiveSpreadsheet().getName())
    Secretaries.getRange(2, 3, 1, 1).setValue(currentUserName.split(" ").shift())
    Secretaries.getRange(2, 2, 1, 1).setValue(currentUserName.split(" ", 2)[1])
    Secretaries.getRange(2, 4, 1, 1).setValue(itemsCharge).setNumberFormat('"$"#,##0.00');
    let secretaryYear = (Number(currentSY())-1).toString() + '-' + (Number(currentSY())).toString();
    let secretaryDescription = `Tech - ${items} ${secretaryYear} SY`
    Secretaries.getRange(2, 7, 1, 1).setValue(secretaryDescription)
    let secretaryDateFormat = ["MM/DD/YYYY"];
    Secretaries.getRange(2, 1, 1, 1).setValue(new Date()).setNumberFormat(secretaryDateFormat)


    missingChargeMessage(currentUser, items, itemsCharge)
    LOG.addTxn(`Successfully charged ${currentUserName} \$${itemsCharge} for their missing ` + textMultiples(items), 'User Charged')

  }
})();

function testCharge() {
  Secretaries.getRange(2, 1, 1, 1).setValue(new Date()).setNumberFormat(secretaryDateFormat)
};

function currentSY() {
  if (new Date().getMonth() < 5) {
    var currentSY = new Date().getFullYear().toString().slice(-2);
  } else {
    var currentSY = (Number(new Date().getFullYear())+1).toString().slice(-2);
  } return currentSY
}

function dailyCheckDue() {
  var today = new Date()
  var tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)
  var oneWeek = new Date(today)
  oneWeek.setDate(oneWeek.getDate() + 7)
  today = toDueString(today);
  tomorrow = toDueString(tomorrow);
  oneWeek = toDueString(oneWeek);

  // Logger.log(today)
  // Logger.log(tomorrow)
  // Logger.log(oneWeek)

  let pastDue = dueTodaysList(today); // Bc remember, we aren't sending emails in the morning if a device is due that day, so the list of devices due today will go out only after they are past due
  let dueTomorrow = daysAccsList(tomorrow);
  let dueOneWeek = daysAccsList(oneWeek);
  pastDue.forEach((account) => {
    ACC.overDue(account)
  })
  dueTomorrow.forEach((account) => dueSoonMessage(account))
  dueOneWeek.forEach((account) => dueSoonMessage(account))

}

function daysAccsList(day) {
  Logger.log(`listing for ${day}`)
  let dueOnDay = Accounts.createTextFinder(day).matchEntireCell(false).findAll()
  // Logger.log(dueOnDay.length)
  
  var accountsList =[];
  for (let i = 0; i < dueOnDay.length; i++) {
    let itemDue = dueOnDay[i]
    let itemRow = itemDue.getRow()
    let itemAcc = Accounts.getRange(itemRow, 1, 1, 1).getValue();
    accountsList.push(itemAcc)
  Logger.log(accountsList)
  }
  accountsList = [...new Set(accountsList)]
  return accountsList
}

function dueTodaysList(today) {
  Logger.log(`listing for today (${today})`)
  let todaysList = Accounts.createTextFinder(today).matchEntireCell(false).findAll()
  var todaysMailingList = [];
  todaysList.forEach((itemRange) => {
    // Logger.log(itemRange.getValue())
    let itemRow = itemRange.getRow()
    let itemAcc = Accounts.getRange(itemRow, 1, 1, 1).getValue();
    let mailTo = [itemAcc]
    if (!todaysMailingList.toString().includes(mailTo)) {
      todaysMailingList.push(mailTo)
    }

    // Logger.log(todaysMailingList)
    let itemName = itemRange.offset(0, -1).getValue();
    // Logger.log(itemName)
    
    if (typeof itemName !== 'string') {
      let numChargersToday = itemRange.getValue().toString().split(`${today}`).length - 1;
      if (numChargersToday == 0) {
        numChargersToday = 1
      }
      itemName = numChargersToday.toString() + ' charger(s)'
    }

    let accountsList = todaysMailingList.map(({[ 0 ]: v }) => v)
    let currentAccountIndex = accountsList.indexOf(itemAcc)
    let currentAccount = todaysMailingList[currentAccountIndex]
    currentAccount.splice (1, 0, itemName)
    // Logger.log(todaysMailingList)
    })
    return todaysMailingList
}

function toDueString(date) {
  var nonZeroedMonth = (new Number(date.getMonth().toString())+1).toString() // I hate Javascript
  var dueString = nonZeroedMonth.padStart(2, 0) + '/' + date.getDate().toString().padStart(2, 0) + '/' + date.getFullYear().toString().slice(2) // So so much
  return dueString
}


function parseDates(cell) {
  var dates = cell.split(",");
  var output = "";
  for (var i = 0; i < dates.length; i++) {
    if (i > 0) {
      output += ", ";
    }
    output += dates[i].trim().toString();
  }
  return output
}