module seidel_method
    implicit none

contains

    subroutine seidel_solve(n, A, b, eps, x)
        implicit none
        integer, intent(in) :: n
        real(8), intent(in) :: A(n,n), b(n), eps
        integer, parameter :: MAX_ITER = 200000
        real(8), intent(out) :: x(n)
        real(8) :: s(n)
        integer :: i, k

        x = 0.0d0
        s = 0.0d0

        do k = 1, MAX_ITER
            do i = n, 1, -1
                x(i) = (b(i) - &
                    sum(A(i, 1:i-1) * x(1:i-1)) - &
                    sum(A(i, i+1:n) * x(i+1:n))) / A(i,i)
            end do
            if (maxval(abs(x - s)) < eps) then
                return 
            end if
            s = x
        end do
    end subroutine seidel_solve 

end module seidel_method