var gulp = require("gulp");
var reload = require("gulp-livereload");
var less = require('gulp-less');

gulp.task('less', function () {
        gulp.src("./*.less")
            .pipe(less())
            .pipe(gulp.dest("./"));
});

gulp.task("watch", function () {
    gulp.watch("./*.less" ,["less"]);
    server = reload();
    gulp.watch(
        './*.less', 
        function (file) {
            server.changed(file.path);
        }
    );
});

gulp.task("default", ["less","watch"]);
