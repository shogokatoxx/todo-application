$('#testModal').on('show.bs.modal',function(event){
  let a = $(event.relatedTarget);
  let target_pk = a.data('deletepk');
  let target_list = target_pk.split('-');
  let modal = $(this);
  modal.find('.delete2').attr('href',target_list[0]+'/task_delete/'+target_list[1]);
});

$('#categoryDelModal').on('show.bs.modal',function(event){
  let deldata = $(event.relatedTarget);
  let pk = deldata.data('deletepk');
  let modal = $(this);
  modal.find('.category-delete').attr('href',pk+'/category_delete');
});

$('#categoryCreUpModal').on('show.bs.modal',function(event){
  let linkdata = $(event.relatedTarget);
  let title = linkdata.data('title');
  if(title === '編集'){
    let pk = linkdata.data('categorypk');
    let text = linkdata.data('text');
    let modal = $(this);
    modal.find('#myModalLabel').text('カテゴリーを'+title);
    modal.find('form').attr('action',pk+'/category_update');
    modal.find('.intext').val(text);
  }else if(title === '追加'){
    let modal = $(this);
    modal.find('#myModalLabel').text('カテゴリーを追加');
    modal.find('form').attr('category_create');
    modal.find('.intext').val('');
  }
});

// const textarea = document.querySelector('textarea');
// textarea.addEventListener('input',()=>{
//   textarea.style.height = "20px";
//   textarea.style.height = textarea.scrollHeight + "px";
// });
const textarea = document.querySelector('textarea');
textarea.addEventListener('input',()=>{
  textarea.style.height = '30px';
  textarea.style.height = textarea.scrollHeight + 'px';
})
