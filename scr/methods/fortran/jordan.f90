module jordan_mod
  implicit none

contains

  subroutine jordan_solve(n, A, b, x)
    integer,  intent(in) :: n
    real(8),  intent(in) :: A(n,n)
    real(8),  intent(in) :: b(n)
    real(8),  intent(out) :: x(n)
    real(8), allocatable :: matrix(:,:), vector_right(:)
    real(8) :: lead_element, mult, temp(n), temp_vec
    integer :: i, k, new_k
    
    allocate(matrix(n,n), vector_right(n))
    matrix = A
    vector_right = b

    do k = 1, n
      new_k = k
      lead_element = abs(matrix(k,k))
      do i = k + 1, n
        if (abs(matrix(i,k)) > lead_element) then
          lead_element = abs(matrix(i,k))
          new_k  = i
        end if
      end do

      if (new_k /= k) then
        temp = matrix(k,:)
        matrix(k,:) = matrix(new_k,:)
        matrix(new_k,:) = temp

        temp_vec = vector_right(k)
        vector_right(k) = vector_right(new_k)
        vector_right(new_k) = temp_vec
      end if

      do i = 1, n
        if (i /= k) then
          mult = matrix(i,k) / matrix(k,k)
          matrix(i,k:n) = matrix(i,k:n) - mult * matrix(k,k:n)
          vector_right(i) = vector_right(i) - mult * vector_right(k)
        end if
      end do
    end do

    do i = 1, n
      x(i) = vector_right(i) / matrix(i,i)
    end do

    deallocate(matrix, vector_right)

  end subroutine jordan_solve

end module jordan_mod