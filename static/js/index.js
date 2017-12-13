let app = angular.module('app', []);
app.controller('controller', ($scope) => {
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
    $.ajax({
      url: '/code',
      type: 'post',
      data: {
        code: $scope.code
      },
      beforeSend: () => $scope.lock = true,
      complete: () => $scope.lock = false,
      success: (data) => {
        if (data.ac) {
          alert('Accept complete!');
        } else {
          alert('Try again!');
        }
      },
      error: () => alert('ERROR')
    });
  };
});
