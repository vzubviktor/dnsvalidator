// copy table to clipboard
function copytable(el) {
         var urlField = document.getElementById(el)   
         var range = document.createRange()
         range.selectNode(urlField)
         window.getSelection().removeAllRanges();
         window.getSelection().addRange(range) 
         document.execCommand('copy')
         }
// switch between tabs         
function chooseTab(evt, tabName) {
         var i, tabcontent, tablinks;
         tabcontent = document.getElementsByClassName("tabcontent");
         for (i = 0; i < tabcontent.length; i++) {
         tabcontent[i].style.display = "none";
         }
         tablinks = document.getElementsByClassName("tablinks");
         for (i = 0; i < tablinks.length; i++) {
         tablinks[i].className = tablinks[i].className.replace(" active", "");
         }
         document.getElementById(tabName).style.display = "block";
         evt.currentTarget.className += " active";
         }
// unhide elements         
function unhide(el) {
         var checkBox = document.getElementById(el);
         var element = document.getElementById("hidden");
         if (checkBox.checked == true){
         element.classList.remove("e-hidden");
         } else {
         element.classList.add("e-hidden");
         }
         }
// download table
function download_csv(csv, filename) {
    var csvFile;
    var downloadLink;

    // CSV FILE
    csvFile = new Blob([csv], {type: "text/csv"});

    // Download link
    downloadLink = document.createElement("a");

    // File name
    downloadLink.download = filename;

    // We have to create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);

    // Make sure that the link is not displayed
    downloadLink.style.display = "none";

    // Add the link to your DOM
    document.body.appendChild(downloadLink);

    // Lanzamos
    downloadLink.click();
}

function export_table_to_csv(html, filename) {
   var csv = [];
   var rows = document.querySelectorAll("table tr");
   
    for (var i = 0; i < rows.length; i++) {
      var row = [], cols = rows[i].querySelectorAll("td, th");
      
        for (var j = 0; j < cols.length; j++) 
            row.push(cols[j].innerText);
        
      csv.push(row.join(","));      
   }

    // Download CSV
    download_csv(csv.join("\n"), filename);
}

document.getElementById("downloadTable").addEventListener("click", function () {
    var html = document.querySelector("table").outerHTML;
   export_table_to_csv(html, "dnscheck.csv");
});
