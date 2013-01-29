/***************************************************************************
 *  Copyright (C) 2011 Binet Réseau                                        *
 *  http://www.polytechnique.fr/eleves/binets/reseau/                      *
 *                                                                         *
 *  This program is free software; you can redistribute it and/or modify   *
 *  it under the terms of the GNU General Public License as published by   *
 *  the Free Software Foundation; either version 2 of the License, or      *
 *  (at your option) any later version.                                    *
 *                                                                         *
 *  This program is distributed in the hope that it will be useful,        *
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
 *  GNU General Public License for more details.                           *
 *                                                                         *
 *  You should have received a copy of the GNU General Public License      *
 *  along with this program; if not, write to the Free Software            *
 *  Foundation, Inc.,                                                      *
 *  59 Temple Place, Suite 330, Boston, MA  02111-1307  USA                *
 ***************************************************************************/

/**
 * AJAXify the aliment search form
 */
var ajax_alimsearch_timer = null;
function ajax_alimsearch_run() {
    ajax_alimsearch_timer = null;
    $.ajax({
        url: barBaseUrl+'/aliments-ajax',
        type: 'GET',
        data: {q_alim: $('#body-form input[name=q_alim]').val()},
        //datatype: 'text',
        success: function(response, status, jqXHR) {
            if (status != "error") {
                $('#body-content').html(response);
                $("#body-header").html(jqXHR.getResponseHeader('X-title'));
            }
        }
    });
}
var alimsearch_lastvalue = '';
function ajax_alimsearch_init() {
    alimsearch_lastvalue = $('#body-form input[name=q_alim]').val();
    $('#body-form input[name=q_alim]').keyup(function() {
        var newvalue = $('#body-form input[name=q_alim]').val();
        if (newvalue == alimsearch_lastvalue)
            return;
        alimsearch_lastvalue = newvalue;
        if (ajax_alimsearch_timer != null)
            clearTimeout(ajax_alimsearch_timer);
        ajax_alimsearch_timer = setTimeout(ajax_alimsearch_run, 30);
    });
}

/**
 * Give focus to te first input element
 */
function focus_init() {
    var e = $('#body-content input[type!=checkbox][type!=hidden][class!=histchange]:first');
    if (window.location.hash == "#money")
        e = $('#money-focus');

    if (e.size() == 0 || e.hasClass('wwh-btn')) {
        $('#body-form input:first').focus();
    } else {
        e.focus().select();
    }
}

/**
 * We-were-hungry checkbox
 */
function wwh_init() {
    var e = $('li#wwh-menu');
    if (e.size() != 1)
        return;
    chk = $('<input type="checkbox" id="wwh-chkbox" />')
        .prop('checked', e.hasClass('wwh-active'))
        .change(function(evt){
            $("li#wwh-menu").css('background-color', '#ddd');
            $.ajax({
                url: barBaseUrl+'/we-were-hungry-ajax',
                type: 'GET',
                data: {active: $('#wwh-chkbox').prop('checked')},
                success: function(response, status, jqXHR) {
                    if (response == 'true')
                        $('#wwh-chkbox').prop('checked', true);
                    else if (response == 'false')
                        $('#wwh-chkbox').prop('checked', false);
                    $("li#wwh-menu").css('background-color', '');
                }
            });
        });
    // e.prepend(chk);
    e.children().first().after(chk);
}

$(function() {
    /* Hide Plat/al devel message... */
    $("div#dev").children().hide();

    ajax_alimsearch_init();
    wwh_init();
    focus_init();

    /* Log out on escape */
    $(document).keydown(function(e) {
        if (e.which == 27) {
            var logoutURL = barBaseUrl + '/logout';
            window.location = logoutURL;
            document.location.href = logoutURL;
        }
    });
});
