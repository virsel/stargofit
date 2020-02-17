var button;
function fFlipCard(eButton) {
  button = eButton;
  var iId = eButton.dataset.card;
  console.log(iId);
  $('#' + iId).toggleClass('flipped');
}
