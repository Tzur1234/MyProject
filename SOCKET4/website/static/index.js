$(function() {
    $('#sendBtn').on('click', function(e) {
      let value =  document.getElementById("msg").value
      console.log(value)
      $.getJSON('/run', {val:value},
          function(data) {
      });
      return false;
    });
  });




// $(function () {
//     $('a#test').on('click', function click(e) {
//         // e.preventDefault()
//         console.log("Hello world") 
//         $.getJSON('/run',
//             function (data) {
//                 // var value = document.getElementById("msg").value
//                 console.log("Hello world")               
                
//             });
//         return false;
//     });
// });

// $(function validate(name){
//     if(name.length >= 2){
//         return true;
//     }
//     else{
//         return false;
//     }
// });
