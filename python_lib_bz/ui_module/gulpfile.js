var gulp = require('gulp'),
    less = require('gulp-less'),
    coffee = require('gulp-coffee'),
    cssmin = require('gulp-cssmin'),
    jsmin = require('gulp-jsmin');
    //rename = require('gulp-rename');

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
  //.pipe(rename({suffix: '.min'}))
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
  //.pipe(rename({suffix: '.min'}))
  .pipe(gulp.dest('./'));
});
gulp.task('default', ['less','coffee', 'watch']);
