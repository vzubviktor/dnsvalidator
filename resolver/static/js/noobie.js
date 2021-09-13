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

function unhideCheck(that) {
    if (that.value == "custom") {
        document.getElementById("customOption").style.display = "block";
        document.getElementById("customOptionKey").style.display = "block";
        console.log(document.getElementById.value);
    } else {
        document.getElementById("customOption").style.display = "none";
        document.getElementById("customOptionKey").style.display = "none";
    }
}

function unhide1(el) {
         var checkBox = document.getElementById(el);
         var element = document.getElementById("hidden1");
         if (checkBox.checked == true){
         element.classList.remove("e-hidden");
         } else {
         element.classList.add("e-hidden");
         }
         }

     
function unhideCheck1(that) {
    if (that.id == "customSelector") {
        document.getElementById("customOption1").style.display = "block";
        document.getElementById("customOptionKey1").style.display = "block";

    } else {
        document.getElementById("customOption1").style.display = "none";
        document.getElementById("customOptionKey1").style.display = "none";
    }
}

function  setVal() {
    const customOption = document.getElementById("customOption1").value
    const customOptionKey = document.getElementById("customOptionKey1").value
    const customOutput = customOption+':'+customOptionKey
    document.getElementById("customSelector").value = customOutput


   
   console.log(customOption);

}

function updateInput1(data){
    document.getElementById("customOption1").value = data;
    console.log(data);
}

function updateInput2(data){
    document.getElementById("customOptionKey1").value = data;
    console.log(data);
}