formSurveySelection = $("#form-survey-selection");

formSurveySelection.on("submit", function () {
  selectedOption = $(
    "#form-survey-selection__select-survey-code option:selected"
  );

  formSurveySelection.attr("action", "/survey/" + selectedOption.val());
});
