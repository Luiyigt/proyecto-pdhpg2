(function($) {
    $.fn.extend({
        slimScroll: function(options) {
            var defaults = {
                width: "auto",
                height: "250px",
                size: "7px",
                color: "#000",
                position: "right",
                distance: "1px",
                start: "top",
                opacity: 0.4,
                alwaysVisible: false,
                disableFadeOut: false,
                railVisible: false,
                railColor: "#333",
                railOpacity: 0.2,
                railDraggable: true,
                railClass: "slimScrollRail",
                barClass: "slimScrollBar",
                wrapperClass: "slimScrollDiv",
                allowPageScroll: false,
                wheelStep: 20,
                touchScrollStep: 200,
                borderRadius: "7px",
                railBorderRadius: "7px"
            };

            var o = $.extend(defaults, options);

            return this.each(function() {
                function scrollEvent(e) {
                    if (isOverPanel) {
                        var e = e || window.event;
                        var delta = 0;

                        e.wheelDelta && (delta = -e.wheelDelta / 120);
                        e.detail && (delta = e.detail / 3);

                        var target = e.target || e.srcTarget || e.srcElement;
                        $(target).closest("." + o.wrapperClass).is(wrapper.parent()) && scrollContent(delta, true);

                        e.preventDefault && !releaseScroll && e.preventDefault();
                        releaseScroll || (e.returnValue = false);
                    }
                }

                function scrollContent(y, isWheel, isJump) {
                    releaseScroll = false;
                    var delta = y;
                    var maxTop = bar.outerHeight() - rail.outerHeight();

                    if (isWheel) {
                        delta = parseInt(bar.css("top")) + y * parseInt(o.wheelStep) / 100 * bar.outerHeight();
                        delta = Math.min(Math.max(delta, 0), maxTop);
                        delta = y > 0 ? Math.ceil(delta) : Math.floor(delta);
                        bar.css({ top: delta + "px" });
                    }

                    percentScroll = parseInt(bar.css("top")) / (rail.outerHeight() - bar.outerHeight());
                    delta = percentScroll * (wrapper[0].scrollHeight - wrapper.outerHeight());

                    if (isJump) {
                        delta = y;
                        var offsetTop = delta / wrapper[0].scrollHeight * wrapper.outerHeight();
                        offsetTop = Math.min(Math.max(offsetTop, 0), maxTop);
                        bar.css({ top: offsetTop + "px" });
                    }

                    wrapper.scrollTop(delta);
                    wrapper.trigger("slimscrolling", ~~delta);
                    showBar();
                    hideBar();
                }

                var isOverPanel, isOverBar, isDragg, queueHide, barHeight, percentScroll;
                var minBarHeight = 30;
                var releaseScroll = false;
                var wheelStep = 20;
                var bar, rail, wrapper = $(this);

                // Set initial styling and structure here
                // Additional code for handling mouse events and touch events

            });
        }
    });

    $.fn.extend({ slimscroll: $.fn.slimScroll });
})(jQuery);
