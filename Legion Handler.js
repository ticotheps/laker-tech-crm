const ActiveDuty = SpreadsheetApp.getActive().getSheetByName('Active Duty');
const Reserves = SpreadsheetApp.getActive().getSheetByName('Reserves');
const SickBay = SpreadsheetApp.getActive().getSheetByName('Sick Bay');
const Boneyard = SpreadsheetApp.getActive().getSheetByName('Boneyard');
const MissingInAction = SpreadsheetApp.getActive().getSheetByName('MIA');

let legions = [ActiveDuty, Reserves, SickBay, Boneyard, MissingInAction];

const LGN = new (function () {
  const _checkLegion = (q) => {
    var Current = SpreadsheetApp.getActive().getActiveSheet();
    var assetsInLegion = Current.getRange(1, 1, Current.getLastRow(), 1).getValues()[0];
    return assetsInLegion.findIndex((element) => element.startsWith(q))+1
  };


  const _removeDeviceLegion = (assetTag) => {
    for (let i = 0; i < legions.length; i++) {
      let found = legions[i].createTextFinder(assetTag).findAll()
      for (let j = 0; j < found.length; j++) {
        let asset = found[j].getRow();
        legions[i].deleteRows(asset, 1);
      }
    }
  };


  this.reserves = (deviceId, explanation) => {
    let device = GAM.getDevice(deviceId);
    let deviceName = device.annotatedAssetId.substring(0, 12)
    let newDevice = {
      "annotatedAssetId": `${deviceName} RESERVES`,
      "annotatedUser": "",
      "orgUnitPath": "/Vault/Students"
    }

    if (explanation) {
      newDevice = {
        ...newDevice,
        notes: explanation
      }
    } else {
      newDevice = {
        ...newDevice,
        notes: 'No explanation given'
      }
    }
    // Logger.log(deviceId)
    GAM.updateDevice(deviceId, newDevice);
    GAM.changeDeviceStatus(deviceId, 'disable')
    GAM.wipeDevice(deviceId);

    _removeDeviceLegion(deviceName);

    let certaintyCheck = GAM.getDevice(deviceId).annotatedAssetId;

    let formulas = [["=ArrayFormula(if(isblank($A$2:$A), \"\", split($A$2:$A, \" - \", false)))"]];
    Reserves.getRange(2, 2, 1, 3).clearContent()

    Reserves.insertRowsBefore(2, 1).getRange(2, 1, 1, 1).setValue(certaintyCheck);
    Reserves.getRange(2, 2, 1, 1).setFormula(formulas);
    
  };

  this.missing = (deviceTag, lastAssignedTo) => {
    let deviceId = searchAssetDB(deviceTag)
    let device = GAM.getDevice(deviceId);
    let deviceName = device.annotatedAssetId.substring(0, 12) // 12 includes the dash
    let dateMissing = new Date().toDateString();
    let lastUser = device.recentUsers[0]
    let lastUsed = getLastTime(device)

    let newDevice = {
      "annotatedAssetId": `${deviceName} Marked AWOL ${dateMissing}`,
      "annotatedUser": "",
      "orgUnitPath": "/Vault/Students",
      "notes": `Last assigned to ${lastAssignedTo}/nLast used by ${lastUser} on ${lastUsed}`
    }

    // Logger.log(deviceId)
    GAM.updateDevice(deviceId, newDevice);
    GAM.changeDeviceStatus(deviceId, 'disable')
    GAM.wipeDevice(deviceId);

    _removeDeviceLegion(deviceName);

    let certaintyCheck = GAM.getDevice(deviceId).annotatedAssetId;

    let formulas = [["=ArrayFormula(if(isblank($A$2:$A), \"\", split($A$2:$A, \" - \", false)))"]];
    MissingInAction.getRange(2, 2, 1, 3).clearContent()
    MissingInAction.insertRowsBefore(2, 1).getRange(2, 1, 1, 1).setValue(certaintyCheck);
    MissingInAction.getRange(2, 2, 1, 1).setFormula(formulas);
    
  };

  this.sickBay = (deviceId, faults, explanation) => {
    let device = GAM.getDevice(deviceId);
    let deviceName = device.annotatedAssetId.substring(0, 10) // 10 does not include the dash, if we used dashes here the split in the cell formula between tag and faulty wouldn't work
    let newDevice = {
      "annotatedAssetId": `${deviceName}: Faulty ${faults}`,
      "annotatedUser": "",
      "orgUnitPath": "/Vault/Students"
    }

    if (explanation) {
      newDevice = {
        ...newDevice,
        notes: explanation
      }
    } else {
      newDevice = {
        ...newDevice,
        notes: 'No explanation given'
      }
    }
    // Logger.log(deviceId)
    GAM.updateDevice(deviceId, newDevice);
    GAM.changeDeviceStatus(deviceId, 'disable')
    GAM.wipeDevice(deviceId);

    _removeDeviceLegion(deviceName);

    let certaintyCheck = GAM.getDevice(deviceId).annotatedAssetId;

    let formulas = [["=ArrayFormula(if(isblank($A$2:$A), \"\", split($A$2:$A, \": \", false)))"]];
    SickBay.getRange(2, 2, 1, 3).clearContent()

    SickBay.insertRowsBefore(2, 1).getRange(2, 1, 1, 1).setValue(certaintyCheck);
    SickBay.getRange(2, 2, 1, 1).setFormula(formulas);
    
  };
})();