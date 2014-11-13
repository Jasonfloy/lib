var gulp = require('gulp');
var coffee = require('gulp-coffee');
var watch = require('gulp-watch');

var coffee_path = './*.coffee';


gulp.task('default', function(){
    gulp.run('coffee');
    gulp.watch(coffee_path,['coffee']);
}
);

gulp.task('coffee', function() {
  gulp.src(coffee_path)
    .pipe(coffee({bare: true}))
    .pipe(gulp.dest('./'));
});
