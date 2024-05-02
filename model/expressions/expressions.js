
// year_of_birth
(function(){
 const current_year = new Date().toLocaleDateString("en",{year: "numeric"});
 
 if (year_of_birth < 1900) {
  return 'Year of birth must be after the year 1900';
 }
 
 if (year_of_birth > current_year) {
  return 'Year of birth cannot be greater than the current year';
 }
  
})();