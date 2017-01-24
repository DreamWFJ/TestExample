$(function () {

    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();

    //2.初始化Button的点击事件
    var oButtonInit = new ButtonInit();
    oButtonInit.Init();

});

        var $table = $('#id-for-manage-article'),
            $remove = $('#remove'),
            selections = [];

        function initTable() {
            $table.bootstrapTable({
                height: getHeight(),
                columns: [
                    [
                        {
                            field: 'state',
                            checkbox: true,
                            rowspan: 2,
                            align: 'center',
                            valign: 'middle'
                        }, {
                            title: 'Item ID',
                            field: 'id',
                            rowspan: 2,
                            align: 'center',
                            valign: 'middle',
                            sortable: true,
                            footerFormatter: totalTextFormatter
                        }, {
                            title: 'Item Detail',
                            colspan: 3,
                            align: 'center'
                        }
                    ],
                    [
                        {
                            field: 'name',
                            title: 'Item Name',
                            sortable: true,
                            editable: true,
                            footerFormatter: totalNameFormatter,
                            align: 'center'
                        }, {
                            field: 'price',
                            title: 'Item Price',
                            sortable: true,
                            align: 'center',
                            editable: {
                                type: 'text',
                                title: 'Item Price',
                                validate: function (value) {
                                    value = $.trim(value);
                                    if (!value) {
                                        return 'This field is required';
                                    }
                                    if (!/^\$/.test(value)) {
                                        return 'This field needs to start width $.'
                                    }
                                    var data = $table.bootstrapTable('getData'),
                                        index = $(this).parents('tr').data('index');
                                    console.log(data[index]);
                                    return '';
                                }
                            },
                            footerFormatter: totalPriceFormatter
                        }, {
                            field: 'operate',
                            title: 'Item Operate',
                            align: 'center',
                            events: operateEvents,
                            formatter: operateFormatter
                        }
                    ]
                ]
            });
            // sometimes footer render error.
            setTimeout(function () {
                $table.bootstrapTable('resetView');
            }, 200);
            $table.on('check.bs.table uncheck.bs.table ' +
                    'check-all.bs.table uncheck-all.bs.table', function () {
                $remove.prop('disabled', !$table.bootstrapTable('getSelections').length);

                // save your data, here just save the current page
                selections = getIdSelections();
                // push or splice the selections if you want to save all data selections
            });
            $table.on('expand-row.bs.table', function (e, index, row, $detail) {
                if (index % 2 == 1) {
                    $detail.html('Loading from ajax request...');
                    $.get('LICENSE', function (res) {
                        $detail.html(res.replace(/\n/g, '<br>'));
                    });
                }
            });
            $table.on('all.bs.table', function (e, name, args) {
                console.log(name, args);
            });
            $remove.click(function () {
                var ids = getIdSelections();
                $table.bootstrapTable('remove', {
                    field: 'id',
                    values: ids
                });
                $remove.prop('disabled', true);
            });
            $(window).resize(function () {
                $table.bootstrapTable('resetView', {
                    height: getHeight()
                });
            });
        }

        function getIdSelections() {
            return $.map($table.bootstrapTable('getSelections'), function (row) {
                return row.id
            });
        }

        function responseHandler(res) {
            $.each(res.rows, function (i, row) {
                row.state = $.inArray(row.id, selections) !== -1;
            });
            return res;
        }

        function detailFormatter(index, row) {
            var html = [];
            $.each(row, function (key, value) {
                html.push('<p><b>' + key + ':</b> ' + value + '</p>');
            });
            return html.join('');
        }

        function operateFormatter(value, row, index) {
            return [
                '<a class="like" href="javascript:void(0)" title="Like">',
                '<i class="glyphicon glyphicon-heart"></i>',
                '</a>  ',
                '<a class="remove" href="javascript:void(0)" title="Remove">',
                '<i class="glyphicon glyphicon-remove"></i>',
                '</a>'
            ].join('');
        }

        window.operateEvents = {
            'click .like': function (e, value, row, index) {
                alert('You click like action, row: ' + JSON.stringify(row));
            },
            'click .remove': function (e, value, row, index) {
                $table.bootstrapTable('remove', {
                    field: 'id',
                    values: [row.id]
                });
            }
        };

        function totalTextFormatter(data) {
            return 'Total';
        }

        function totalNameFormatter(data) {
            return data.length;
        }

        function totalPriceFormatter(data) {
            var total = 0;
            $.each(data, function (i, row) {
                total += +(row.price.substring(1));
            });
            return '$' + total;
        }

        function getHeight() {
            return $(window).height() - $('h1').outerHeight(true);
        }

        $(function () {
            var scripts = [
                    location.search.substring(1) || 'assets/bootstrap-table/src/bootstrap-table.js',
                    'assets/bootstrap-table/src/extensions/export/bootstrap-table-export.js',
                    'http://rawgit.com/hhurz/tableExport.jquery.plugin/master/tableExport.js',
                    'assets/bootstrap-table/src/extensions/editable/bootstrap-table-editable.js',
                    'http://rawgit.com/vitalets/x-editable/master/dist/bootstrap3-editable/js/bootstrap-editable.js'
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

            eachSeries(scripts, getScript, initTable);
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
var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_departments').bootstrapTable({
            url: '/manage/article',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: true,                  //是否显示所有的列
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: true
            }, {
                field: 'Name',
                title: '部门名称'
            }, {
                field: 'ParentName',
                title: '上级部门'
            }, {
                field: 'Level',
                title: '部门级别'
            }, {
                field: 'Desc',
                title: '描述'
            }, ]
        });
    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            departmentname: $("#txt_search_departmentname").val(),
            statu: $("#txt_search_statu").val()
        };
        return temp;
    };
    return oTableInit;
};


var ButtonInit = function () {
    var oInit = new Object();
    var postdata = {};

    oInit.Init = function () {
        //初始化页面上面的按钮事件
    };

    return oInit;
};