butt.addEventListener('click',function(){
  document.querySelector('.btn').innerHTML="LOADING..."
})
logkro=()=>{
  document.querySelector('.btn').innerHTML="PROGRAM STARTED"
  document.querySelector('.btn').style.color = 'rgb(10, 230, 72)';

}
butt.addEventListener('click',function(){
  setTimeout(logkro,5500)
})