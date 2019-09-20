const main_header = document.getElementsByClassName('special')[0]
var i = -1;
var colorArr = ["blue","white","yellow","red",""];
console.log(main_header);
main_header.style.color 
window.setInterval(function() {
  i++;
  main_header.style.color = colorArr[i];
  // When we get to the end we loop back around :) wow js CAN be fun.
  if (i == 3) {
    i = 0;
  }
},500);
