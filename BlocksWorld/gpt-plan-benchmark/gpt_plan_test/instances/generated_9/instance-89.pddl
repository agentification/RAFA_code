

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a g)
(on b e)
(on c d)
(ontable d)
(on e h)
(on f c)
(on g f)
(ontable h)
(on i a)
(clear b)
(clear i)
)
(:goal
(and
(on a e)
(on b g)
(on c a)
(on d h)
(on e d)
(on f i)
(on g f))
)
)


