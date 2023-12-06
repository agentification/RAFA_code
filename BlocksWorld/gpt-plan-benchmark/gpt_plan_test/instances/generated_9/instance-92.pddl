

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b c)
(on c e)
(on d g)
(on e d)
(ontable f)
(on g f)
(on h i)
(on i a)
(clear b)
(clear h)
)
(:goal
(and
(on a e)
(on b a)
(on c d)
(on f c)
(on g b)
(on h i)
(on i f))
)
)


