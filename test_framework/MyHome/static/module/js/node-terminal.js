/**
 * Created by WFJ on 2016/12/2.
 */
var anim = false;
function typed(finish_typing) {
    return function(term, message, delay, finish) {
        anim = true;
        var prompt = term.get_prompt();
        var c = 0;
        if (message.length > 0) {
            term.set_prompt('');
            var interval = setInterval(function() {
                term.insert(message[c++]);
                if (c == message.length) {
                    clearInterval(interval);
                    // execute in next interval
                    setTimeout(function() {
                        // swap command with prompt
                        finish_typing(term, message, prompt);
                        anim = false;
                        finish && finish();
                    }, delay);
                }
            }, delay);
        }
    };
}
var typed_prompt = typed(function(term, message, prompt) {
    // swap command with prompt
    term.set_command('');
    term.set_prompt(message + ' ');
});
var typed_message = typed(function(term, message, prompt) {
    term.set_command('');
    term.echo(message);
    term.set_prompt(prompt);
});



var instance_id;
var instance_terminal;
function init_terminal(_id){
    instance_terminal = $('#terminal_cmd_interactive').terminal(function(cmd, term){
        instance_id = _id;
        var finish = false;
        var msg = "Waitting for server response...";
        term.set_prompt('> ');
        typed_message(term, msg, 50, function() {
            finish = true;
        });
        var args = {command: cmd, _id:_id};
        console.log('1',term.paused());
        $.get('/terminal/interact', args, function(result) {
            (function wait() {
                if (finish) {
                    if(result.status){
                        term.echo(result.message);
                    }else {
                        term.error("ERROR: " + result.message)
                    }

                } else {
                    setTimeout(wait, 500);
                }
            })();
            console.log('2',term.paused())
        }, 'json');
    }, {
        name: 'node',
        greetings: null,
        width: 500,
        height: 300,

        onInit: function(term) {
            // first question
            term.echo("Init server...");
            term.echo('');
            instance_id = _id;
            $.get("/terminal/interact", {command: 'init', _id:_id}, function(result){
                //var result = $.parseJSON(result);
                term.echo(result.message);
                if(! result.status){
                    $("#node_realtime_status").removeClass("glyphicon-ok-sign").addClass("glyphicon-remove-sign").css("color", "red");
                    term.echo("please click reconnect");
                    term.disable();
                    term.pause();

                    //term.freeze()
                } else {
                    $("#node_realtime_status").removeClass("glyphicon-remove-sign").addClass("glyphicon-ok-sign").css("color", "green");
                    term.resume();
                    term.enable();
                    term.echo("Please Input Command");
                }

            }, "json");
        },
        keydown: function(e, term) {
            if (anim) {
                return false;
            }
        }
    });
}
function resetTerminal(){
    instance_terminal.reset();
}

var current_node_id;
function init_terminal_module_data(_id){
    current_node_id = _id;
    $.get("/node/terminal/data", {_id:_id}, function(result) {
        if (result instanceof Object){
            $("#terminal_node_name").text(result.node.node_name);
            $("#terminal_node_ip").text(result.node.node_ip);
            html = "";
            var task_lists = result.task_lists;
            for(one in task_lists){
                html += '<option value="'+task_lists[one]._id+'">'+task_lists[one].task_name+'</option>'
            }
            $("#associated_task").html(html);
        }

    }, "json");
}

jQuery(function($) {
    // 手动执行脚本
    $("#execute_task_in_node").on("click", function(){
        var selected = [];
        $('#associated_task option:selected').each(function() {
            selected.push([$(this).val(), $(this).data('order')]);
        });

        var text = '';
        for (var i = 0; i < selected.length; i++) {
            text += selected[i][0] + ', ';
        }
        text = text.substring(0, text.length - 2);

        $.post("/node/terminal/data", {task_id:text, node_id:current_node_id}, function(result) {
            console.log(result);
            instance_terminal.echo(result.msg);
        }, "json");

    });
    $('#terminalCmdInteractiveModal').on('hidden.bs.modal', function (e) {
        instance_terminal.purge();
        instance_terminal.destroy();
        $.ajax({
            url: "/terminal/interact?_id="+instance_id,
            type: "DELETE",
            success: function(r){
                console.log(r);
            }
        });
        $table.bootstrapTable('refresh');
    });

});

function executeTaskInNode(){
    var selected = [];
    $('#associated_task option:selected').each(function() {
        selected.push([$(this).val(), $(this).data('order')]);
    });

    var text = '';
    for (var i = 0; i < selected.length; i++) {
        text += selected[i][0] + ', ';
    }
    text = text.substring(0, text.length - 2);
    console.log(text);
}