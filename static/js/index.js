let app = angular.module('app', []);
app.controller('controller', ($scope, $http) => {
  $scope.lock = false;
  $scope.code =
`#include <stdio.h>

int main(int argc, char **argv)
{
    int a, b;
    scanf("%d %d", &a, &b);
    printf("%d", a + b);
    return 0;
}`;
  $scope.submitCode = () => {
    $scope.lock = true;
    $http.post('/code', $.param({code: $scope.code}), {
      headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    }).then((response) => {
      if (response.data.ac) {
        alert('Accept complete!');
      } else {
        alert('Try again!');
      }
      $scope.lock = false;
    });
  };
});
