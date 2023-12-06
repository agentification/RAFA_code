

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a h)
(on b i)
(on c e)
(on d f)
(on e a)
(ontable f)
(on g b)
(ontable h)
(on i c)
(clear d)
(clear g)
)
(:goal
(and
(on a g)
(on b h)
(on c f)
(on d a)
(on f d)
(on g e)
(on h c)
(on i b))
)
)


