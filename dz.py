#Static Folder Name
foldername = "getskills" 

dz_array = {
        "public":{
            "favicon":f"{foldername}/images/favicon.png",
            "description":"Neper CodingKidz : Online Learning Admin",
            "og_title":"Neper CodingKidz : Online Learning Admin",
            "og_description":"Neper CodingKidz : Online Learning Admin",
            "og_image":"https://getskills.dexignzone.com/django/social-image.png",
            "title":"Neper CodingKidz Online Learning Admin",
        },
        "global":{
            "css":[
                    f"{foldername}/vendor/jquery-nice-select/css/nice-select.css",
                    f"{foldername}/css/style.css"
                ],

            "js":{
                "top":[
                    f"{foldername}/vendor/global/global.min.js",
                    f"{foldername}/vendor/jquery-nice-select/js/jquery.nice-select.min.js",
                ],
                "bottom":[
                    f"{foldername}/js/custom.js",
                    f"{foldername}/js/dlabnav-init.js",

                ]
            },

        },
        "pagelevel":{
            "getskills":{#AppName
                "getskills_views":{
                    "css":{
                        "index":[
                            f"{foldername}/vendor/bootstrap-datetimepicker/css/bootstrap-datetimepicker.min.css"
                        ],
                        "index2":[
                            f"{foldername}/vendor/bootstrap-datetimepicker/css/bootstrap-datetimepicker.min.css"
                        ],
                        "schedule":[
                            f"{foldername}/vendor/bootstrap-datetimepicker/css/bootstrap-datetimepicker.min.css",
                            f"{foldername}/vendor/fullcalendar/css/main.min.css"
                        ],
                        "instructors":[],
                        "message":[],
                        "activity":[],
                        "profile":[],

                        "permissions":[
                            f"{foldername}/vendor/sweetalert2/dist/sweetalert2.min.css", 
                        ],

                        "users":[
                            f"{foldername}/vendor/sweetalert2/dist/sweetalert2.min.css",    
                        ],
                        "add_user":[
                            f"{foldername}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                            f"{foldername}/vendor/select2/css/select2.min.css",
                        ],
                        "edit_user":[
                            f"{foldername}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                            f"{foldername}/vendor/select2/css/select2.min.css",
                        ],
                        "groups_list":[
                            f"{foldername}/vendor/sweetalert2/dist/sweetalert2.min.css",
                        ],
                        "assign_permissions_to_user":[

                            f"{foldername}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/prettify.min.css",
                            f"{foldername}/vendor/bootstrap-duallistbox/src/bootstrap-duallistbox.css",
                            f"{foldername}/vendor/bootstrap-duallistbox/dist/bootstrap-duallistbox.css",
                        ],

                        "group_add":[
                            f"{foldername}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/prettify.min.css",
                            f"{foldername}/vendor/bootstrap-duallistbox/src/bootstrap-duallistbox.css",
                            f"{foldername}/vendor/bootstrap-duallistbox/dist/bootstrap-duallistbox.css",
                        ],


                        "group_edit":[
                            f"{foldername}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/prettify.min.css",
                            f"{foldername}/vendor/bootstrap-duallistbox/src/bootstrap-duallistbox.css",
                            f"{foldername}/vendor/bootstrap-duallistbox/dist/bootstrap-duallistbox.css",
                        ],







                        "courses":[
                            f"{foldername}/vendor/swiper/css/swiper-bundle.min.css"
                        ],
                        "course_details_1":[
                            f"{foldername}/vendor/magnific-popup/magnific-popup.min.css",
                        ],
                        "course_details_2":[
                            f"{foldername}/vendor/magnific-popup/magnific-popup.min.css",
                        ],
                        "instructor_dashboard":[
                            f"{foldername}/vendor/bootstrap-datetimepicker/css/bootstrap-datetimepicker.min.css",
                        ],
                        "instructor_courses":[
                            f"{foldername}/vendor/owl-carousel/owl.carousel.css",
                        ],
                        "instructor_schedule":[
                            f"{foldername}/vendor/fullcalendar/css/main.min.css",
                        ],
                        "instructor_students":[
                            f"{foldername}/vendor/datatables/css/jquery.dataTables.min.css",
                        ],
                        "instructor_resources":[],
                        "instructor_transactions":[
                            f"{foldername}/vendor/datatables/css/jquery.dataTables.min.css",
                        ],
                        "instructor_liveclass":[],
                        "app_profile":[
                            f"{foldername}/vendor/lightgallery/css/lightgallery.min.css",
                            f"{foldername}/vendor/magnific-popup/magnific-popup.css"
                        ],
                        "post_details":[
                            f"{foldername}/vendor/lightgallery/css/lightgallery.min.css",
                            f"{foldername}/vendor/magnific-popup/magnific-popup.css"
                        ],
                        "email_compose":[
                            f"{foldername}/vendor/dropzone/dist/dropzone.css",
                        ],
                        "email_inbox":[],
                        "email_read":[],
                        "app_calender":[
                            f"{foldername}/vendor/fullcalendar/css/main.min.css",
                        ],

                        "ecom_product_grid":[],
                        "ecom_product_list":[
                            f"{foldername}/vendor/star-rating/star-rating-svg.css",
                        ],
                        "ecom_product_detail":[
                            f"{foldername}/vendor/star-rating/star-rating-svg.css",
                        ],
                        "ecom_product_order":[],
                        "ecom_checkout":[],
                        "ecom_invoice":[
                            f"{foldername}/vendor/bootstrap-select/dist/css/bootstrap-select.min.css",
                        ],
                        "ecom_customers":[],

                        "chart_float":[],
                        "chart_morris":[],
                        "chart_chartjs":[],
                        "chart_chartist":[
                            f"{foldername}/vendor/chartist/css/chartist.min.css"
                        ],
                        "chart_sparkline":[],
                        "chart_peity":[],
                        "uc_select2":[
                            f"{foldername}/vendor/select2/css/select2.min.css",
                        ],
                        "uc_nestable":[
                            f"{foldername}/vendor/nestable2/css/jquery.nestable.min.css"
                        ],
                        "uc_noui_slider":[
                            f"{foldername}/vendor/nouislider/nouislider.min.css"
                        ],
                        "uc_sweetalert":[
                            f"{foldername}/vendor/sweetalert2/dist/sweetalert2.min.css"
                        ],
                        "uc_toastr":[
                            f"{foldername}/vendor/toastr/css/toastr.min.css"
                        ],
                        "map_jqvmap":[
                            f"{foldername}/vendor/jqvmap/css/jqvmap.min.css"
                        ],
                        "uc_lightgallery":[
                            f"{foldername}/vendor/lightgallery/css/lightgallery.min.css"
                        ],
                        "widget_basic":[
                            f"{foldername}/vendor/chartist/css/chartist.min.css",
                            f"{foldername}/vendor/bootstrap-select/dist/css/bootstrap-select.min.css",
                        ],
                        "form_element":[],
                        "form_wizard":[
                            f"{foldername}/vendor/jquery-smartwizard/dist/css/smart_wizard.min.css"
                        ],
                        "form_ckeditor":[],
                        "form_pickers":[
                            f"{foldername}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                            f"{foldername}/vendor/clockpicker/css/bootstrap-clockpicker.min.css",
                            f"{foldername}/vendor/jquery-asColorPicker/css/asColorPicker.min.css",
                            f"{foldername}/vendor/bootstrap-material-datetimepicker/css/bootstrap-material-datetimepicker.css",
                            f"{foldername}/vendor/pickadate/themes/default.css",
                            f"{foldername}/vendor/pickadate/themes/default.date.css",
                        ],
                        "form_validation":[],
                        "table_bootstrap_basic":[],
                        "table_datatable_basic":[
                            f"{foldername}/vendor/datatables/css/jquery.dataTables.min.css",
                        ],
                        "page_login":[],
                        "page_register":[],
                        "page_forgot_password":[],
                        "page_lock_screen":[],
                        "page_error_400":[],
                        "page_error_403":[],
                        "page_error_404":[],
                        "page_error_500":[],
                        "page_error_503":[],
                        "empty_page":[],
                    },
                    "js":{
                        "index":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/apexchart/apexchart.js",
                            f"{foldername}/vendor/bootstrap-datetimepicker/js/moment.js",
                            f"{foldername}/vendor/bootstrap-datetimepicker/js/bootstrap-datetimepicker.min.js",
                            f"{foldername}/js/dashboard/dashboard-1.js",
                        ],
                        "index2":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/apexchart/apexchart.js",
                            f"{foldername}/vendor/bootstrap-datetimepicker/js/moment.js",
                            f"{foldername}/vendor/bootstrap-datetimepicker/js/bootstrap-datetimepicker.min.js",
                            f"{foldername}/js/dashboard/dashboard-1.js",
                        ],
                        "schedule":[
                            f"{foldername}/vendor/bootstrap-datetimepicker/js/moment.js",
                            f"{foldername}/vendor/bootstrap-datetimepicker/js/bootstrap-datetimepicker.min.js",
                            f"{foldername}/vendor/apexchart/apexchart.js",
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/moment/moment.min.js",
                            f"{foldername}/vendor/fullcalendar/js/main.min.js",
                            f"{foldername}/js/plugins-init/fullcalendar-init.js",
                            f"{foldername}/js/dashboard/schedule.js",
                            
                        ],
                        "instructors":[],
                        "message":[],
                        "activity":[],
                        "profile":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/apexchart/apexchart.js",
                            f"{foldername}/vendor/peity/jquery.peity.min.js",
                            f"{foldername}/js/dashboard/my-profile.js",
                        ],





                        "permissions":[
                            f"{foldername}/vendor/sweetalert2/dist/sweetalert2.min.js",
                        ],

                        "users":[
                            f"{foldername}/vendor/sweetalert2/dist/sweetalert2.min.js",
                        ],
                        "add_user":[
                            f"{foldername}/vendor/moment/moment.min.js",
                            f"{foldername}/vendor/bootstrap-daterangepicker/daterangepicker.js",
                            f"{foldername}/vendor/select2/js/select2.full.min.js",
                            f"{foldername}/js/plugins-init/select2-init.js"
                        ],
                        "edit_user":[
                            f"{foldername}/vendor/moment/moment.min.js",
                            f"{foldername}/vendor/bootstrap-daterangepicker/daterangepicker.js",
                            f"{foldername}/vendor/select2/js/select2.full.min.js",
                            f"{foldername}/js/plugins-init/select2-init.js"
                        ],
                        "groups_list":[
                            f"{foldername}/vendor/sweetalert2/dist/sweetalert2.min.js",
                        ],
                        "assign_permissions_to_user":[
                            f"{foldername}/vendor/bootstrap-duallistbox/ajax/libs/popper.js/1.12.9/umd/popper.min.js",
                            f"{foldername}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/run_prettify.js",
                            f"{foldername}/vendor/bootstrap-duallistbox/dist/jquery.bootstrap-duallistbox.js",
                        ],
                        "group_add":[
                            f"{foldername}/vendor/bootstrap-duallistbox/ajax/libs/popper.js/1.12.9/umd/popper.min.js",
                            f"{foldername}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/run_prettify.js",
                            f"{foldername}/vendor/bootstrap-duallistbox/dist/jquery.bootstrap-duallistbox.js",
                        ],

                        "group_edit":[
                            f"{foldername}/vendor/bootstrap-duallistbox/ajax/libs/popper.js/1.12.9/umd/popper.min.js",
                            f"{foldername}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/run_prettify.js",
                            f"{foldername}/vendor/bootstrap-duallistbox/dist/jquery.bootstrap-duallistbox.js",
                        ],









                        "courses":[
                            f"{foldername}/vendor/swiper/js/swiper-bundle.min.js",
                            f"{foldername}/js/dlab.carousel.js"
                        ],
                        "course_details_1":[
                            f"{foldername}/vendor/magnific-popup/magnific-popup.js"
                        ],
                        "course_details_2":[
                            f"{foldername}/vendor/magnific-popup/magnific-popup.js"
                        ],
                        "instructor_dashboard":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/apexchart/apexchart.js",
                            f"{foldername}/vendor/bootstrap-datetimepicker/js/moment.js",
                            f"{foldername}/vendor/bootstrap-datetimepicker/js/bootstrap-datetimepicker.min.js",
                            f"{foldername}/vendor/day-fullcalendar/main.min.js",
                            f"{foldername}/vendor/peity/jquery.peity.min.js",
                            f"{foldername}/js/dashboard/instructor-dashboard.js",
                        ],
                        "instructor_courses":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/apexchart/apexchart.js",
                            f"{foldername}/vendor/peity/jquery.peity.min.js",
                            f"{foldername}/vendor/owl-carousel/owl.carousel.js",
                            f"{foldername}/js/dashboard/instructor-courses.js",
                            f"{foldername}/js/dlab.carousel.js",
                        ],
                        "instructor_schedule":[
                            f"{foldername}/vendor/moment/moment.min.js",
                            f"{foldername}/vendor/fullcalendar/js/main.min.js",
                            f"{foldername}/js/plugins-init/fullcalendar-init.js"
                        ],
                        "instructor_students":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/apexchart/apexchart.js",
                            f"{foldername}/vendor/datatables/js/jquery.dataTables.min.js",
                            f"{foldername}/js/plugins-init/datatables.init.js",
                            f"{foldername}/vendor/owl-carousel/owl.carousel.js",
                            f"{foldername}/js/dashboard/instructor-student.js",
                        ],
                        "instructor_resources":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                        ],
                        "instructor_transactions":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/apexchart/apexchart.js",
                            f"{foldername}/vendor/datatables/js/jquery.dataTables.min.js",
                            f"{foldername}/js/plugins-init/datatables.init.js",
                            f"{foldername}/js/dashboard/instructor-transactions.js",
                        ],
                        "instructor_liveclass":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                        ],
                        "app_profile":[
                             f"{foldername}/vendor/lightgallery/js/lightgallery-all.min.js",
                             f"{foldername}/vendor/magnific-popup/magnific-popup.js"
                        ],
                        "post_details":[
                            f"{foldername}/vendor/lightgallery/js/lightgallery-all.min.js",
                            f"{foldername}/vendor/magnific-popup/magnific-popup.js"
                        ],
                        "email_compose":[
                            f"{foldername}/vendor/dropzone/dist/dropzone.js",
                        ],
                        "email_inbox":[],
                        "email_read":[],
                        "app_calender":[
                            f"{foldername}/vendor/moment/moment.min.js",
                            f"{foldername}/vendor/fullcalendar/js/main.min.js",
                            f"{foldername}/js/plugins-init/fullcalendar-init.js",
                        ],
                        "ecom_product_grid":[],
                        "ecom_product_list":[
                            f"{foldername}/vendor/star-rating/jquery.star-rating-svg.js", 
                        ],
                        "ecom_product_detail":[
                            f"{foldername}/vendor/star-rating/jquery.star-rating-svg.js",
                        ],
                        "ecom_product_order":[],
                        "ecom_checkout":[],
                        "ecom_invoice":[],
                        "ecom_customers":[],

                        "chart_flot":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/apexchart/apexchart.js",
                            f"{foldername}/vendor/flot/jquery.flot.js",
                            f"{foldername}/vendor/flot/jquery.flot.pie.js",
                            f"{foldername}/vendor/flot/jquery.flot.resize.js",
                            f"{foldername}/vendor/flot-spline/jquery.flot.spline.min.js",
                            f"{foldername}/js/plugins-init/flot-init.js",
                        ],
                        "chart_morris":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/apexchart/apexchart.js",
                            f"{foldername}/vendor/raphael/raphael.min.js",
                            f"{foldername}/vendor/morris/morris.min.js",
                            f"{foldername}/js/plugins-init/morris-init.js",
                        ],
                        "chart_chartjs":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/js/plugins-init/chartjs-init.js",
                        ],
                        "chart_chartist":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/apexchart/apexchart.js",
                            f"{foldername}/vendor/chartist/js/chartist.min.js",
                            f"{foldername}/vendor/chartist-plugin-tooltips/js/chartist-plugin-tooltip.min.js",
                            f"{foldername}/js/plugins-init/chartist-init.js",
                        ],
                        "chart_sparkline":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/apexchart/apexchart.js",
                            f"{foldername}/vendor/jquery-sparkline/jquery.sparkline.min.js",
                            f"{foldername}/js/plugins-init/sparkline-init.js",
                            f"{foldername}/vendor/svganimation/vivus.min.js",
                            f"{foldername}/vendor/svganimation/svg.animation.js"
                        ],
                        "chart_peity":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/peity/jquery.peity.min.js",
                            f"{foldername}/js/plugins-init/piety-init.js",
                        ],

                        "uc_select2":[
                            f"{foldername}/vendor/select2/js/select2.full.min.js",
                            f"{foldername}/js/plugins-init/select2-init.js"
                        ],
                        "uc_nestable":[
                            f"{foldername}/vendor/nestable2/js/jquery.nestable.min.js",
                            f"{foldername}/js/plugins-init/nestable-init.js"

                        ],
                        "uc_noui_slider":[
                            f"{foldername}/vendor/nouislider/nouislider.min.js",
                            f"{foldername}/vendor/wnumb/wNumb.js",
                            f"{foldername}/js/plugins-init/nouislider-init.js"
                        ],
                        "uc_sweetalert":[
                            f"{foldername}/vendor/sweetalert2/dist/sweetalert2.min.js",
                            f"{foldername}/js/plugins-init/sweetalert.init.js",

                        ],
                        "uc_toastr":[
                            f"{foldername}/vendor/toastr/js/toastr.min.js",
                            f"{foldername}/js/plugins-init/toastr-init.js"
                        ],
                        "map_jqvmap":[
                            f"{foldername}/vendor/jqvmap/js/jquery.vmap.min.js",
                            f"{foldername}/vendor/jqvmap/js/jquery.vmap.world.js",
                            f"{foldername}/vendor/jqvmap/js/jquery.vmap.usa.js",
                            f"{foldername}/js/plugins-init/jqvmap-init.js"

                        ],
                        "uc_lightgallery":[
                            f"{foldername}/vendor/lightgallery/js/lightgallery-all.min.js"

                        ],
                        "widget_basic":[
                            f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                            f"{foldername}/vendor/apexchart/apexchart.js",
                            f"{foldername}/vendor/chartist/js/chartist.min.js",
                            f"{foldername}/vendor/chartist-plugin-tooltips/js/chartist-plugin-tooltip.min.js",
                            f"{foldername}/vendor/flot/jquery.flot.js",
                            f"{foldername}/vendor/flot/jquery.flot.pie.js",
                            f"{foldername}/vendor/flot/jquery.flot.resize.js",
                            f"{foldername}/vendor/flot-spline/jquery.flot.spline.min.js",
                            f"{foldername}/vendor/jquery-sparkline/jquery.sparkline.min.js",
                            f"{foldername}/js/plugins-init/sparkline-init.js",
                            f"{foldername}/vendor/peity/jquery.peity.min.js",
                            f"{foldername}/js/plugins-init/piety-init.js",
                            f"{foldername}/js/plugins-init/widgets-script-init.js",
                        ],
                    "form_element":[],
                    "form_wizard":[
                        f"{foldername}/vendor/jquery-steps/build/jquery.steps.min.js",
                        f"{foldername}/vendor/jquery-validation/jquery.validate.min.js",
                        f"{foldername}/js/plugins-init/jquery.validate-init.js",
                        f"{foldername}/vendor/jquery-smartwizard/dist/js/jquery.smartWizard.js",
                    ],
                    "form_ckeditor":[
                        f"{foldername}/vendor/ckeditor/ckeditor.js"
                    ],
                    "form_pickers":[
                         f"{foldername}/vendor/bootstrap-select/dist/js/bootstrap-select.min.js",
                         f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                         f"{foldername}/vendor/apexchart/apexchart.js",
                         f"{foldername}/vendor/moment/moment.min.js",
                         f"{foldername}/vendor/bootstrap-daterangepicker/daterangepicker.js",
                         f"{foldername}/vendor/clockpicker/js/bootstrap-clockpicker.min.js",
                         f"{foldername}/vendor/jquery-asColor/jquery-asColor.min.js",
                         f"{foldername}/vendor/jquery-asGradient/jquery-asGradient.min.js",
                         f"{foldername}/vendor/jquery-asColorPicker/js/jquery-asColorPicker.min.js",
                         f"{foldername}/vendor/bootstrap-material-datetimepicker/js/bootstrap-material-datetimepicker.js",
                         f"{foldername}/vendor/pickadate/picker.js",
                         f"{foldername}/vendor/pickadate/picker.time.js",
                         f"{foldername}/vendor/pickadate/picker.date.js",
                         f"{foldername}/js/plugins-init/bs-daterange-picker-init.js",
                         f"{foldername}/js/plugins-init/clock-picker-init.js",
                         f"{foldername}/js/plugins-init/jquery-asColorPicker.init.js",
                         f"{foldername}/js/plugins-init/material-date-picker-init.js",
                         f"{foldername}/js/plugins-init/pickadate-init.js",
                    ],
                    "form_validation":[],
                    "table_bootstrap_basic":[],
                    "table_datatable_basic":[
                        f"{foldername}/vendor/chart.js/Chart.bundle.min.js",
                        f"{foldername}/vendor/apexchart/apexchart.js",
                        f"{foldername}/vendor/datatables/js/jquery.dataTables.min.js",
                        f"{foldername}/js/plugins-init/datatables.init.js",
                    ],
                    "page_login":[],
                    "page_register":[],
                    "page_forgot_password":[],
                    "page_lock_screen":[],
                    "page_error_400":[],
                    "page_error_403":[],
                    "page_error_404":[],
                    "page_error_500":[],
                    "page_error_503":[],
                    "empty_page":[],


                    },
                }
            }
        }


}