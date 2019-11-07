$('#testModal').on('show.bs.modal',function(event){
  var a = $(event.relatedTarget);
  var target_pk = a.data('deletepk');
  var modal = $(this);
  modal.find('.delete2').attr('href','delete2/'+target_pk);
});
