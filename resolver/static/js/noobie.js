 function copytable(el) {
         var urlField = document.getElementById(el)   
         var range = document.createRange()
         range.selectNode(urlField)
         window.getSelection().removeAllRanges();
         window.getSelection().addRange(range) 
         document.execCommand('copy')
         }
         
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
         
function unhide(el) {
         var checkBox = document.getElementById(el);
         var element = document.getElementById("hidden");
         if (checkBox.checked == true){
         element.classList.remove("e-hidden");
         } else {
         element.classList.add("e-hidden");
         }
         }