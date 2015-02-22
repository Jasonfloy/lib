//var gulp = require('gulp');
//var coffee = require('gulp-coffee');
//var watch = require('gulp-watch');
//var less = require('gulp-less');
//
//var coffee_path = './*.coffee';
//var less_path = './*.less';
//
//
//gulp.task('default', function(){
//    gulp.run('coffee');
//    gulp.watch('*',['coffee', 'less']);
//}
//);
//
//gulp.task('coffee', function() {
//  gulp.src(coffee_path)
//    .pipe(coffee({bare: true}))
//    .pipe(gulp.dest("./"));
//});
//
//gulp.task('less', function () {
//        gulp.src(less_path)
//            .pipe(less())
//            .pipe(gulp.dest("./"));
//});
var gulp = require('gulp'),
    less = require('gulp-less'),
    coffee = require('gulp-coffee'),
    cssmin = require('gulp-cssmin'),
    jsmin = require('gulp-jsmin'),
    rename = require('gulp-rename');

gulp.task('watch', function () {
  gulp.watch('./*.less', ['less']);
  gulp.watch('./*.coffee', ['coffee']);
});

gulp.task('less', function () {
  return gulp.src('./*.less')
  .pipe(less().on('error', function (err) {
    console.log(err);
  }))
  .pipe(cssmin().on('error', function(err) {
    console.log(err);
  }))
  .pipe(rename({suffix: '.min'}))
  .pipe(gulp.dest('./'));

});

gulp.task('coffee', function () {
  return gulp.src('./*.coffee')
  .pipe(coffee().on('error', function (err) {
    console.log(err);
  }))
  //.pipe(jsmin().on('error', function(err) {
  //  console.log(err);
  //}))
  .pipe(rename({suffix: '.min'}))
  .pipe(gulp.dest('./'));
});
gulp.task('default', ['less','coffee', 'watch']);
