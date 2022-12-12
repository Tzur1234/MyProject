var messages = "";
// global veriable

$(function () {
  $("#sendBtn").on("click", function () {
    var msg = document.getElementById("msg");
    var value = msg.value;
    msg.value = "";
    $.getJSON("/run", { val: value }, function (data) {});
  });
});

window.onload = function () {
  // run update function every 1000 milsecondes
  var update_loop = setInterval(update, 3000);
  update()
  
};


function update(){
  fetch(`${window.origin}/send_list_back`)
  .then(function (response) {

    if (response.status !== 200) {
      console.log("Response status wasn't 200")
      return ;
    }
    response.json().then(function (data) {
      console.log(data)
      var messages = "";
      for(value of data["messages"]){
        messages = messages + "<br>" + value
      }
      console.log(messages)
      document.getElementById("test").innerHTML = messages
    })

  })

}





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
