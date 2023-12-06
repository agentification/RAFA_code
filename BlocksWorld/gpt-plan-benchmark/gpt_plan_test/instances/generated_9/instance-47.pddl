

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b i)
(on c d)
(on d f)
(on e c)
(ontable f)
(on g h)
(ontable h)
(on i e)
(clear a)
(clear b)
(clear g)
)
(:goal
(and
(on b h)
(on d c)
(on e a)
(on g e)
(on i g))
)
)


