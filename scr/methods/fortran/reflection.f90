module reflection_method
    implicit none

contains

    subroutine reflection_solve(n, A_orig, b_orig, x)
        integer,  intent(in) :: n
        real(8),  intent(in) :: A_orig(n,n)
        real(8),  intent(in) :: b_orig(n)
        real(8),  intent(out) :: x(n)
        real(8), allocatable :: x_col(:), normal_vec(:, :)
        real(8) :: A(n,n), b(n), norma, summa = 0
        integer :: i, k, val
        
        A = A_orig
        b = b_orig

        do k = 1, n - 1
            val = n + 1 - k
            allocate(x_col(val), normal_vec(val, 1))

            x_col = A(k:n , k)
            norma = sqrt(sum(x_col * x_col))
            if (A(k, k) >= 0.0d0) then 
                x_col(1) = x_col(1) + norma
                normal_vec(:, 1) = x_col(1:val)
            else
                x_col(1) = x_col(1) - norma
                normal_vec(:, 1) = x_col(1:val)
            end if 
            A(k:n, k:n) = A(k:n, k:n) - (2 / sum(x_col * x_col))*matmul(normal_vec, matmul(transpose(normal_vec), A(k:n, k:n)))
            b(k:n) = b(k:n) - (2 / sum(x_col * x_col))*matmul(normal_vec, matmul(transpose(normal_vec), b(k:n)))
            deallocate(x_col, normal_vec)
        end do
        x(n) = b(n) / A(n, n)
        do k = n - 1, 1, -1
            do i = n, k + 1, -1
                summa = summa + A(k, i) * x(i)
            end do
            x(k) = (b(k) - summa) / A(k, k)
            summa = 0
        end do
    end subroutine reflection_solve            
end module reflection_method