

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a f)
(ontable b)
(on c b)
(on d c)
(ontable e)
(ontable f)
(on g e)
(ontable h)
(on i d)
(clear a)
(clear g)
(clear h)
(clear i)
)
(:goal
(and
(on b i)
(on c a)
(on d e)
(on e h)
(on f c)
(on i d))
)
)


