

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b d)
(ontable c)
(ontable d)
(on e a)
(on f g)
(on g b)
(on h f)
(on i e)
(clear c)
(clear h)
(clear i)
)
(:goal
(and
(on a f)
(on b d)
(on c a)
(on d h)
(on f g)
(on g i)
(on i e))
)
)


