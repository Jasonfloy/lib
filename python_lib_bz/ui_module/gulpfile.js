var gulp = require('gulp');
var coffee = require('gulp-coffee');
var watch = require('gulp-watch');
var less = require('gulp-less');

var coffee_path = './*.coffee';
var less_path = './*.less';


gulp.task('default', function(){
    gulp.run('coffee');
    gulp.watch('*',['coffee', 'less']);
}
);

gulp.task('coffee', function() {
  gulp.src(coffee_path)
    .pipe(coffee({bare: true}))
    .pipe(gulp.dest("./"));
});

gulp.task('less', function () {
        gulp.src(less_path)
            .pipe(less())
            .pipe(gulp.dest("./"));
});
