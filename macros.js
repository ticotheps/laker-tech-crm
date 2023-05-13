function dinero() {
  var spreadsheet = SpreadsheetApp.getActive();
  spreadsheet.getRange('C2').activate();
  spreadsheet.getActiveRangeList().setNumberFormat('_("$"* #,##0.00_);_("$"* \\(#,##0.00\\);_("$"* "-"??_);_(@_)');
};