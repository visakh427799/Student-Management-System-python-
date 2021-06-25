
const login=()=>{

    let username=document.getElementById('uname').value;
    let password=document.getElementById('pass').value;
    let btn=document.getElementById('loginbtn')
    let loader=document.getElementById('login-loader')
    if(username&&password){
       btn.style.display="hidden"
       
        $.ajax({
            data : {
               username :username ,
               password:password ,
                   },
               type : 'POST',
               url : '/admin/login'
              })
          .done(function(data) {
            if(data.status){
                console.log(data.status);
               

            }
        });


    }
    
}