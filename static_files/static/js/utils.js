// Utility function

function Util() { };




/* 

	class manipulation functions

*/




Util.hasClass = function (el, className) {

    if (el.classList) return el.classList.contains(className);

    else {
        if (el.className)
            return !!el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'));
        else
            return !!el.attr('class').match(new RegExp('(\\s|^)' + className + '(\\s|$)'));
    }
};



Util.addClass = function (el, className) {

    var classList = className.split(' ');

    if (el.classList) el.classList.add(classList[0]);


    else if (!Util.hasClass(el, classList[0])) {
        if (!el.className)
            el.attr('class') += ' ' + classList[0];
        else
            el.className += " " + classList[0];
    }
    if (classList.length > 1) Util.addClass(el, classList.slice(1).join(' '));

};





Util.removeClass = function (el, className) {

    var classList = className.split(' ');

    if (el.classList) el.classList.remove(classList[0]);

    else if (Util.hasClass(el, classList[0])) {

        var reg = new RegExp('(\\s|^)' + classList[0] + '(\\s|$)');

        el.className = el.className.replace(reg, ' ');

    }

    if (classList.length > 1) Util.removeClass(el, classList.slice(1).join(' '));

};

Util.changeSelectedStatus = function (el) {
    var currentClasses = el.getAttribute('class');

    var ClassList = currentClasses.split(' ');
    var SelectedClassName = '';
    SelectedClassName = ClassList.find(function (string) {
        var regex = new RegExp('.*selected.*');
        if (string.match(regex))
            return string;
        else
            return '';
    })
  
    if (SelectedClassName == '' || typeof SelectedClassName == 'undefined') {
        var newClassName = ClassList[0] + '-selected';
        Util.addClass(el, newClassName);
    }
    else {
        Util.removeClass(el, SelectedClassName);
    }
}


Util.switchClass = function (el, currentClass, newClass) {
    Util.removeClass(el, currentClass);
    Util.addClass(el, newClass);
}

Util.toggleClass = function (el, className, bool) {

    if (bool) Util.addClass(el, className);

    else Util.removeClass(el, className);

};


var dElements = {}
Util.fSetExpandedStandardClassName = function (el, sClass_name_add) {
    var sId = el.getAttribute('id');
    if (!dElements[sId]) {
        var sClassName = el.getAttribute('class');
        dElements[sId] = sClassName;
        el.setAttribute('class', sClassName + ' ' + sClass_name_add);
       
    }
    else {
     
        el.setAttribute('class', dElements[sId] + ' ' + sClass_name_add);
        
    }
}




Util.setAttributes = function (el, attrs) {

    for (var key in attrs) {

        el.setAttribute(key, attrs[key]);

    }

};



/* 

  DOM manipulation

*/

Util.getChildrenByClassName = function (el, className) {

    var children = el.children,

        childrenByClass = [];

    for (var i = 0; i < el.children.length; i++) {

        if (Util.hasClass(el.children[i], className)) childrenByClass.push(el.children[i]);

    }

    return childrenByClass;

};



/* 

	Animate height of an element

*/

Util.setHeight = function (start, to, element, duration, cb) {

    var change = to - start,

        currentTime = null;



    var animateHeight = function (timestamp) {

        if (!currentTime) currentTime = timestamp;

        var progress = timestamp - currentTime;

        var val = parseInt((progress / duration) * change + start);

        element.setAttribute("style", "height:" + val + "px;");

        if (progress < duration) {

            window.requestAnimationFrame(animateHeight);

        } else {

            cb();

        }

    };



    //set the height of the element before starting animation -> fix bug on Safari

    element.setAttribute("style", "height:" + start + "px;");

    window.requestAnimationFrame(animateHeight);

};



/* 

	Smooth Scroll

*/



Util.scrollTo = function (final, duration, cb) {

    var start = window.scrollY || document.documentElement.scrollTop,

        currentTime = null;



    var animateScroll = function (timestamp) {

        if (!currentTime) currentTime = timestamp;

        var progress = timestamp - currentTime;

        if (progress > duration) progress = duration;

        var val = Math.easeInOutQuad(progress, start, final - start, duration);

        window.scrollTo(0, val);

        if (progress < duration) {

            window.requestAnimationFrame(animateScroll);

        } else {

            cb && cb();

        }

    };



    window.requestAnimationFrame(animateScroll);

};



/* 

  Focus utility classes

*/



//Move focus to an element

Util.moveFocus = function (element) {

    if (!element) element = document.getElementsByTagName("body")[0];

    element.focus();

    if (document.activeElement !== element) {

        element.setAttribute('tabindex', '-1');

        element.focus();

    }

};



/* 

  Misc

*/



Util.getIndexInArray = function (array, el) {

    return Array.prototype.indexOf.call(array, el);

};



Util.cssSupports = function (property, value) {

    if ('CSS' in window) {

        return CSS.supports(property, value);

    } else {

        var jsProperty = property.replace(/-([a-z])/g, function (g) { return g[1].toUpperCase(); });

        return jsProperty in document.body.style;

    }

};



/* 

	Polyfills

*/

//Closest() method

if (!Element.prototype.matches) {

    Element.prototype.matches = Element.prototype.msMatchesSelector || Element.prototype.webkitMatchesSelector;

}



if (!Element.prototype.closest) {

    Element.prototype.closest = function (s) {

        var el = this;

        if (!document.documentElement.contains(el)) return null;

        do {

            if (el.matches(s)) return el;

            el = el.parentElement || el.parentNode;

        } while (el !== null && el.nodeType === 1);

        return null;

    };

}



//Custom Event() constructor

if (typeof window.CustomEvent !== "function") {



    function CustomEvent(event, params) {

        params = params || { bubbles: false, cancelable: false, detail: undefined };

        var evt = document.createEvent('CustomEvent');

        evt.initCustomEvent(event, params.bubbles, params.cancelable, params.detail);

        return evt;

    }



    CustomEvent.prototype = window.Event.prototype;



    window.CustomEvent = CustomEvent;

}



/* 

	Animation curves

*/

Math.easeInOutQuad = function (t, b, c, d) {

    t /= d / 2;

    if (t < 1) return c / 2 * t * t + b;

    t--;

    return -c / 2 * (t * (t - 2) - 1) + b;

};