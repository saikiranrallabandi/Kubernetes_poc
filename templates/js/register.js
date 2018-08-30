$(document).ready(function(){

$(function () {
    vm = new viewModel();
    ko.applyBindings(vm);

    //Bootstrap tooltip
    $('#password').tooltip({
        placement: "right"
    });
});

//Apply validation for password strength
$('#register-form').parsley({
    validators: {
        uppercount: function (val, uppers) {
            return countContain(val, m_strUpperCase) >= uppers
        },
        lowercount: function (val, lowers) {
            return countContain(val, m_strLowerCase) >= lowers
        },
        numcount: function (val, nums) {
            return countContain(val, m_strNumber) >= nums
        }
    },
    messages: {
        uppercount: "Must be at least %s uppercase character",
        lowercount: "Must be at least %s lowercase character ",
        numcount: "Must be at least %s number"
    }
});

function viewModel() {
    var self = this;
    self.registerEmail = ko.observable();
    self.registerPassword = ko.observable();
    self.confirmPassword = ko.observable();
    self.agree = ko.observable(false);

    self.register = function () {
        $("#register-form").submit();
    };
}


//Count number of uppercase, lowercase, numeric and special characters
var m_strUpperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
var m_strLowerCase = "abcdefghijklmnopqrstuvwxyz";
var m_strNumber = "0123456789";
var m_strCharacters = "!@#$%^&*?_~";
function countContain(strPassword, strCheck) {
    // Declare variables
    var nCount = 0;

    for (i = 0; i < strPassword.length; i++) {
        if (strCheck.indexOf(strPassword.charAt(i)) > -1) {
            nCount++;
        }
    }

    return nCount;
}
});