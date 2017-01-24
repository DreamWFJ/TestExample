/**
 * Created by WFJ on 2016/12/1.
 */
var NODE_TASK_API_URL = "/node/timetask/data";

var $node_time_task_table = $('#id-for-manage-node-timetask'),
    $alert = $('.alert').hide(),
    $btn_node_task_delete = $('#btn_node_task_delete'),
    selections = [],
    $batch_add_time_tasks = $('#batchAddTimeTasksForm'),
    $batch_add_time_tasks_modal = $('#batch_add_time_tasks_modal').modal({show: false});


// 设置弹出对话框属性
$(document).ready(function() {
    $("#btn_node_task_add").on("click", function(){
        $batch_add_time_tasks.attr("action", "/node/timetask/data");
    });
    // 弹出框中设置执行周期单位
    $("#select_time_task_period_unit").children("li").each(function(){
        $(this).children("a").on("click", function(){
            var unit_value = $(this).text();
            $("#set_time_task_period_unit").text(unit_value);
            $("#time_task_period_unit").val(unit_value).text(unit_value);
        })
    });

    // 初始化查询平台中 是否周期执行单选按钮
    $("#txt_search_is_period_execute").multiselect();
    // 时间格式化
    $('#first_execute_time')
        .datetimepicker({
            weekStart: 1,
            format: "yyyy-mm-dd HH:ii:ss",
            todayBtn:  true,
            autoclose: true,
            todayHighlight: 1,
            startView: 2,
            forceParse: 0,
            pickerPosition: "bottom-left"
        })

        .on('dp.change dp.show', function(e) {
            // Validate the date when user change it
            $batch_add_time_tasks
            // Get the bootstrapValidator instance
            .data('bootstrapValidator')
            // Mark the field as not validated, so it'll be re-validated when the user change date
            .updateStatus('first_execute_time', 'NOT_VALIDATED', null)
            // Validate the field
            .validateField('first_execute_time');
        });

    // 多选初始化
    $batch_add_time_tasks.find('[name="node_ids"]')
            // 初始化多选
            .multiselect({
                includeSelectAllOption: true,
                selectAllValue: 'select-all-value',
                // Re-validate the multiselect field when it is changed
                onChange: function(element, checked) {
                    $batch_add_time_tasks
                        .data('bootstrapValidator')                 // Get plugin instance
                        .updateStatus('node_ids', 'NOT_VALIDATED')  // Update field status
                        .validateField('node_ids');                 // and re-validate it
                }
            })
            .end();
    $batch_add_time_tasks.find('[name="time_task_ids"]')
            // 初始化多选
            .multiselect({
                includeSelectAllOption: true,
                selectAllValue: 'select-all-value',
                // Re-validate the multiselect field when it is changed
                onChange: function(element, checked) {
                    $batch_add_time_tasks
                        .data('bootstrapValidator')                 // Get plugin instance
                        .updateStatus('time_task_ids', 'NOT_VALIDATED')  // Update field status
                        .validateField('time_task_ids');                 // and re-validate it
                }
            })
            .end();
    // 添加校验
    $batch_add_time_tasks.bootstrapValidator({
        // Exclude only disabled fields
        // The invisible fields set by Bootstrap Multiselect must be validated
        excluded: [':disabled'],
        live: 'enable',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            node_ids: {
                validators: {
                    callback: {
                        message: 'Please choose more than 1 node you use for binding',
                        callback: function(value, validator) {
                            // Get the selected options
                            var options = validator.getFieldElements('node_ids').val();
                            return (options != null && options.length >= 1);
                        }
                    }
                }
            },
            time_task_ids: {
                validators: {
                    callback: {
                        message: 'Please choose more than 1 task you use for binding',
                        callback: function(value, validator) {
                            // Get the selected options
                            var options = validator.getFieldElements('time_task_ids').val();
                            return (options != null && options.length >= 1);
                        }
                    }
                }
            },
            first_execute_time: {
                validators: {
                    validators: {
                        notEmpty: {
                            message: 'The first execute time is required and cannot be empty'
                        },
                        date: {
                            format: 'yyyy-mm-dd HH:ii:ss'
                        }
                    }
                }
            },
            time_task_period_num: {
                validators: {
                    enabled: false,
                    trigger: 'keyup',
                    validators: {
                        notEmpty: {
                            message: 'The time task period number is required and cannot be empty'
                        },
                        digits: {
                            message: 'The time task period number is not valid'
                        }
                    }
                }
            }
        }
    });




    // toggle开关设置
    $batch_add_time_tasks.find('[name="is_period_execute"]')
        .bootstrapSwitch({
            size: 'small',
            state: true, //设置初始状态
            onText: "YES",
            offText: "NO",
            // 添加change事件处理
            onSwitchChange: function(event, state) {
                var time_task_period = $("#time_task_period");
                console.log(state);
                state ? time_task_period.find("input").removeAttr('disabled')
                      : time_task_period.find("input").attr('disabled', 'disabled');
                state ? time_task_period.find("button").removeAttr('disabled')
                      : time_task_period.find("button").attr('disabled', 'disabled');

                if (state){
                    $batch_add_time_tasks
                        .data('bootstrapValidator')
                        .enableFieldValidators('time_task_period_num', state)
                        .updateStatus('time_task_period_num', 'NOT_VALIDATED')  // Update field status
                        .validateField('time_task_period_num');
                } else {
                    $batch_add_time_tasks
                        .data('bootstrapValidator')
                        .enableFieldValidators('time_task_period_num', state)
                }

                //var bootstrapValidator = $('#BatchAddTimeTaskForm').data('bootstrapValidator');
                //$("#manual_set_time_task_config").toggle(!state);
                //// 开启对该字段的校验
                //bootstrapValidator.enableFieldValidators('first_execute_time', !state)
                //              .enableFieldValidators('time_task_period_num', !state);


            },
            // 初始化
            onInit: function(event, state){


            }
        });

});



function queryParamsNodeTimeTaskTable(params) {
    return {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
        limit: params.limit,   //页面大小
        offset: params.offset,  //页码
        order: params.order,
        sort: params.sort,
        start_time: $("#txt_search_start_time").val(),
        end_time: $("#txt_search_end_time").val(),
        search_id: $("#txt_search_ID").val(),
        is_period_execute: $("#txt_search_is_period_execute").val()
    };
}

function initNodeTimeTaskTable() {
    $node_time_task_table.bootstrapTable({
        //height: getHeight(),
        queryParams: queryParamsNodeTimeTaskTable,//传递参数（*）
        columns: [
        [
            {
                field: 'state',
                checkbox: true,
                rowspan: 2,
                align: 'center',
                valign: 'middle'
            },
            {
                title: 'Item ID',
                field: '_id',
                rowspan: 2,
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                title: 'Item Detail',
                colspan: 6,
                align: 'center'
            }
        ],
        [
            {
                field: 'node_id',
                title: 'Node ID',
                sortable: true,
                align: 'left'
            },{
                field: 'task_id',
                title: 'Task ID',
                sortable: true,
                align: 'left'
            },{
                field: 'first_execute_time',
                title: 'First Execute Time',
                sortable: false,
                formatter: firstExecuteTimeFormatter,
                align: 'left'
            },{
                field: 'is_period_execute',
                title: 'Is Period Execute',
                sortable: false,
                formatter: isPeriodExecuteFormatter,
                align: 'center'
            }, {
                field: 'execute_period',
                title: 'Execute Period',
                sortable: true,
                align: 'left',
                formatter: executePeriodFormatter,
                editable: false
            },{
                field: 'operate',
                title: 'Operate',
                align: 'center',
                clickToSelect: false,
                events: operateEvents,
                formatter: operateFormatter
            }
        ]]

    });
    // sometimes footer render error.
    setTimeout(function () {
        $node_time_task_table.bootstrapTable('resetView');
    }, 200);
    $node_time_task_table.on('check.bs.table uncheck.bs.table ' +
            'check-all.bs.table uncheck-all.bs.table', function () {
        $btn_node_task_delete.prop('disabled', !$node_time_task_table.bootstrapTable('getSelections').length);
        selections = getIdSelections();
        // push or splice the selections if you want to save all data selections
    });


    $btn_node_task_delete.click(function () {
        var ids = getIdSelections();
        if (!deleteNodeTaskItems(ids.join(','))) return;
        $node_time_task_table.bootstrapTable('remove', {
            field: '_id',
            values: ids
        });

        $btn_node_task_delete.prop('disabled', true);
    });

    $(window).resize(function () {
        $node_time_task_table.bootstrapTable('resetView', {
            height: getHeight()
        });
    });
}

// 启动表格
$(function () {
    var scripts = [
        location.search.substring(1) || '/static/js/bootstrap/bootstrap-table/bootstrap-table.min.js',
        '/static/js/bootstrap/bootstrap-table/extensions/bootstrap-table-export.js',
        '/static/js/bootstrap/bootstrap-table/extensions/tableExport.js',
        '/static/js/bootstrap/bootstrap-table/extensions/bootstrap-table-editable.js',
        '/static/js/bootstrap/bootstrap-table/extensions/bootstrap-editable.js'
    ],
    eachSeries = function (arr, iterator, callback) {
        callback = callback || function () {};
        if (!arr.length) {
            return callback();
        }
        var completed = 0;
        var iterate = function () {
            iterator(arr[completed], function (err) {
                if (err) {
                    callback(err);
                    callback = function () {};
                }
                else {
                    completed += 1;
                    if (completed >= arr.length) {
                        callback(null);
                    }
                    else {
                        iterate();
                    }
                }
            });
        };
        iterate();
    };

    eachSeries(scripts, getScript, initNodeTimeTaskTable);
});

function getScript(url, callback) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.src = url;

    var done = false;
    // Attach handlers for all browsers
    script.onload = script.onreadystatechange = function() {
        if (!done && (!this.readyState ||
                this.readyState == 'loaded' || this.readyState == 'complete')) {
            done = true;
            if (callback)
                callback();

            // Handle memory leak in IE
            script.onload = script.onreadystatechange = null;
        }
    };

    head.appendChild(script);

    // We handle everything using the script element injection
    return undefined;
}

function nodeTimeTaskRefreshTable(){
    $node_time_task_table.bootstrapTable('refresh');
}


// 选中的ID
function getIdSelections() {
    return $.map($node_time_task_table.bootstrapTable('getSelections'), function (row) {
        return row._id;
    });
}


// 表格中定义的响应句柄
function responseHandler(res) {
    $.each(res.rows, function (i, row) {
        row.state = $.inArray(row._id, selections) !== -1;
    });
    return res;
}

// 表格中小加号点击后内容展现方式定义
function detailFormatter(index, row) {
    var html = [];
    $.each(row, function (key, value) {
        html.push('<p><b>' + key + ' :</b> ' + value + '</p>');
    });
    return html.join('');
}

// 表格中首次执行时间格式化
function firstExecuteTimeFormatter(value, row, index) {
    var last_time;
    if (value){
        last_time = new Date(parseInt(value) * 1000).toLocaleString();
    } else {
        last_time = "--";
    }
    return last_time;
}

// 表格中是否周期执行格式化
function isPeriodExecuteFormatter(value, row, index) {
    var return_html = "";
    if (value == 1){
        return_html = '<span style="color: green"><i class="glyphicon glyphicon-ok-sign"></i></span>';
    } else {
        return_html = '<span style="color: red"><i class="glyphicon glyphicon-remove-sign"></i></span>'
    }
    return return_html;
}

// 表格中周期格式化
function executePeriodFormatter(value, row, index) {
    return [
        '<span>',
        row.time_task_period_num,
        '</span>',
        '<span style="color: green">',
        row.time_task_period_unit,
        '</span>'
    ].join(' ')
}

// 表格中操作动作格式定义
function operateFormatter(value, row, index) {
    return [
        '<a class="update text-warning" href="javascript:void(0)" title="Update Task">',
        '<i class="glyphicon glyphicon-pencil"></i>',
        '</a>  ',
        '<a class="remove text-danger" href="javascript:void(0)" title="Remove Task">',
        '<i class="glyphicon glyphicon-remove"></i>',
        '</a>'
    ].join('');
}



window.operateEvents = {
    'click .update': function (e, value, row, index) {
        console.log("click update, do nothing.");
        $batch_add_time_tasks.attr("action", "/node/timetask/data?_id="+row._id);
        showUpdateTimeTaskModal($(this).attr('title'), row);
        $batch_add_time_tasks_modal.modal('show');
    },
    'click .remove': function (e, value, row, index) {
        deleteNodeTaskItems(row._id);
    }
};

function windowOpen(url, target){
　　var a = document.createElement("a");
　　a.setAttribute("href", url);
　　if(target == null){
　　  target = '';
　　}
　　a.setAttribute("target", target);
　　document.body.appendChild(a);
　　if(a.click){
　　  a.click();
　　}else{
    　　try{
        　　var evt = document.createEvent('Event');
        　　a.initEvent('click', true, true);
        　　a.dispatchEvent(evt);
    　　}catch(e){
    　　  window.open(url);
    　　}
　　}
　　document.body.removeChild(a);
}


function deleteNodeTaskItems(ids){
    bootbox.confirm({
        size: "small",
        onEscape: true,
        backdrop: true,
        message: 'Are you sure ?',
        callback: function(result){
            if(result){
                $.ajax({
                    url: NODE_TASK_API_URL +'?_id=' + ids,
                    type: 'delete',
                    success: function () {
                        $node_time_task_table.bootstrapTable('refresh');
                        showAlert('Delete item successful!', 'success');
                        return true;
                    },
                    error: function () {
                        showAlert('Delete item error!', 'danger');
                    }
                })
            }
        }
    });
    return false;
}

function getHeight() {
    return $(window).height() - $('h1').outerHeight(true);
}

// 显示更新对话框
function showUpdateTimeTaskModal(title, row) {
    row = row || {
        _id: '',
        task_id: '',
        node_id: '',
        first_execute_time: '',
        is_period_execute: '',
        time_task_period_num: '',
        time_task_period_unit: ''
    }; // default row value
    console.log(row.node_id);
    $batch_add_time_tasks_modal.data('_id', row._id);
    $batch_add_time_tasks_modal.find('.modal-title').text(title);
    // 多选初始化
    $('#node_ids').multiselect('select', row.node_id, true);
    // 设置禁止更改
    $('#node_ids').multiselect('disable');
    $('#time_task_ids').multiselect('select', row.task_id, true);
    $('#time_task_ids').multiselect('disable');
    if (row.first_execute_time && row.first_execute_time != ''){
        $batch_add_time_tasks.find('[name="first_execute_time"]').val(new Date(parseInt(row.first_execute_time) * 1000).toLocaleString());
    }else {
        $batch_add_time_tasks.find('[name="first_execute_time"]').val("");
    }

    //$batch_add_time_tasks.find('[name="is_period_execute"]').bootstrapSwitch('setState', Boolean(row.is_period_execute));
    if(row.is_period_execute == 1){
        // toggle开关设置

        //$("#is_period_execute").bootstrapSwitch('setState', true);
        //$("#is_period_execute").attr("checked", true);
        $batch_add_time_tasks.find('[name="time_task_period_num"]').val(row.time_task_period_num);
        $batch_add_time_tasks.find('[name="time_task_period_unit "]').val(row.time_task_period_unit);
        $("#set_time_task_period_unit").text(row.time_task_period_unit);
    }else{
        //$("#is_period_execute").bootstrapSwitch('setState', false);
        //$("#is_period_execute").removeAttr("checked");
        $batch_add_time_tasks.find('[name="time_task_period_num"]').val("");
        $batch_add_time_tasks.find('[name="time_task_period_unit "]').val("");
    }
}
